export const meta = {
  name: 'log-diagnosis-multi-service',
  description: 'Fan out CloudWatch log diagnosis across multiple services: scan + pattern-match per service, enrich unmatched errors via aws-knowledge MCP',
  whenToUse: 'When log-diagnosis scope is multiple services or the whole account. Single-service diagnosis does not need this — run the skill inline.',
  phases: [
    { title: 'Scan', detail: 'one agent per service: run query-logs.sh, match error-patterns.yaml, classify' },
    { title: 'Enrich', detail: 'one agent per service with unmatched errors: query aws-knowledge MCP for likely cause' },
  ],
}

// ─────────────────────────────────────────────────────────────────────────
// CONTRACT (args)
//
// This workflow is the fan-out engine for the log-diagnosis skill's
// "multi-service / global" path. The skill's main agent MUST scope first
// (Step 0: confirm services, time range, region; resolve log groups from
// environments/<account>/account.yaml `log_sources`), then pass the resolved
// scope here. The workflow does NOT ask the user anything.
//
// args = {
//   account_id:  string,                 // e.g. "123456789012" (REQUIRED)
//   region:      string,                 // e.g. "us-east-1" (default ap-northeast-1)
//   hours_back:  number,                 // default 1
//   skill_dir:   string,                 // REQUIRED — abs path to the log-diagnosis skill dir
//   services: [                          // resolved by the main agent
//     {
//       name:       string,              // service name (service_catalog key)
//       log_groups: string[] | undefined // resolved log group names; if omitted,
//                                        //   the scan agent discovers them via
//                                        //   describe-log-groups + log-source-map.md
//     },
//     ...
//   ]
// }
//
// RETURNS { scope, services: [ <scan result, optionally + enrichment> ] }
// The main agent renders the final report from this using
// assets/diagnosis-template.md. Report writing stays in the main loop on
// purpose — it needs the template and human-facing judgment.
// ─────────────────────────────────────────────────────────────────────────

// skill_dir and account_id are REQUIRED — no defaults are baked in, so this
// workflow carries no environment-specific paths or account numbers. The
// log-diagnosis main agent supplies them when it invokes the workflow.
const SKILL_DIR = args && args.skill_dir
const ACCOUNT = args && args.account_id
const REGION = (args && args.region) || 'ap-northeast-1'
const HOURS = (args && args.hours_back) || 1
const SERVICES = (args && Array.isArray(args.services)) ? args.services : []

if (!SKILL_DIR) {
  throw new Error('args.skill_dir is required (absolute path to the log-diagnosis skill directory).')
}
if (!ACCOUNT) {
  throw new Error('args.account_id is required.')
}
if (!SERVICES.length) {
  throw new Error(
    'No services in args. The log-diagnosis main agent must resolve scope ' +
    '(services + log_groups from account.yaml log_sources) before invoking this workflow.'
  )
}

const QUERY_SCRIPT = `${SKILL_DIR}/scripts/query-logs.sh`
const ERROR_PATTERNS = `${SKILL_DIR}/references/error-patterns.yaml`
const QUERY_TEMPLATES = `${SKILL_DIR}/references/query-templates.md`
const LOG_SOURCE_MAP = `${SKILL_DIR}/references/log-source-map.md`

// Structured output of the Scan stage (one per service).
const SCAN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['service', 'region', 'log_groups_queried', 'findings', 'scan_notes'],
  properties: {
    service: { type: 'string' },
    region: { type: 'string' },
    log_groups_queried: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'exists', 'stored_bytes', 'results_returned'],
        properties: {
          name: { type: 'string' },
          exists: { type: 'boolean' },
          stored_bytes: { type: 'number' },
          results_returned: { type: 'number' },
        },
      },
    },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: [
          'error_signature', 'sample_message', 'count',
          'first_seen', 'last_seen', 'matched_pattern_id',
          'severity', 'likely_cause', 'time_distribution', 'source_log_group',
        ],
        properties: {
          error_signature: { type: 'string', description: 'normalized representative form of the error' },
          sample_message: { type: 'string', description: 'one raw log line, verbatim from query output' },
          count: { type: 'number' },
          first_seen: { type: 'string' },
          last_seen: { type: 'string' },
          matched_pattern_id: {
            type: ['string', 'null'],
            description: 'id from error-patterns.yaml, or null if no known pattern matched',
          },
          severity: { type: 'string', enum: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'] },
          likely_cause: { type: 'string' },
          time_distribution: { type: 'string', enum: ['burst', 'sustained', 'increasing', 'sparse'] },
          source_log_group: { type: 'string' },
        },
      },
    },
    scan_notes: {
      type: 'string',
      description: 'caveats: empty log groups, query timeouts, zero errors, Container Insights not enabled, etc.',
    },
  },
}

// Structured output of the Enrich stage (one per service that has unmatched findings).
const ENRICH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['service', 'enriched'],
  properties: {
    service: { type: 'string' },
    enriched: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['error_signature', 'proposed_cause', 'proposed_severity', 'sources', 'confidence'],
        properties: {
          error_signature: { type: 'string' },
          proposed_cause: { type: 'string', description: 'grounded in MCP docs; say so if MCP returned nothing' },
          proposed_severity: { type: 'string', enum: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN'] },
          sources: { type: 'array', items: { type: 'string' }, description: 'MCP doc URLs / SOP names actually used' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
      },
    },
  },
}

function scanPrompt(svc) {
  const lgLine = (svc.log_groups && svc.log_groups.length)
    ? `Pre-resolved log groups for this service:\n${svc.log_groups.map(g => `  - ${g}`).join('\n')}`
    : `No log groups were pre-resolved. Discover them: read ${LOG_SOURCE_MAP}, then run ` +
      `\`aws logs describe-log-groups --log-group-name-prefix ... --region ${REGION}\` to confirm real names. ` +
      `Never invent a log group name.`

  return [
    `You are diagnosing CloudWatch logs for ONE service in a read-only AWS investigation.`,
    `Account: ${ACCOUNT}   Region: ${REGION}   Service: ${svc.name}   Window: last ${HOURS}h.`,
    ``,
    lgLine,
    ``,
    `Procedure:`,
    `1. For each log group, confirm it exists and has data:`,
    `   \`aws logs describe-log-groups --log-group-name-prefix "<name>" --region ${REGION}\`.`,
    `   If storedBytes == 0, record it in scan_notes and skip querying it (group exists but is empty).`,
    `2. Run the error scan. Use the verified templates in ${QUERY_TEMPLATES} — do NOT hand-write Insights queries.`,
    `   Start with template 1b (error detail, case-insensitive) and 1a (count by 5m bin for trend).`,
    `   Execute via the wrapper, e.g.:`,
    `     bash ${QUERY_SCRIPT} --multi-groups "<g1,g2>" 'filter @message like /(?i)(error|exception|fatal|critical)/ | fields @timestamp, @message, @logStream | sort @timestamp desc' ${HOURS} ${REGION} --limit 100`,
    `   The script outputs JSON (results, statistics) on stdout.`,
    `3. From the query output, identify DISTINCT error signatures (normalize variable bits like ids/timestamps).`,
    `   Match each against the regex patterns in ${ERROR_PATTERNS}. Set matched_pattern_id to the matching`,
    `   pattern's id, or null if none matches. Take severity + likely_cause from the matched pattern; if unmatched,`,
    `   make your best classification and mark matched_pattern_id null (it will be enriched downstream).`,
    `4. For each finding, read the 5m-bin counts to set time_distribution: burst (concentrated at one point),`,
    `   sustained (even across the window), increasing (worsening), or sparse (few isolated hits).`,
    ``,
    `Hard rules (this is an anti-hallucination investigation):`,
    `- Every finding MUST trace to actual query output. sample_message must be a verbatim line from the results.`,
    `- Do NOT report errors you did not see in the output. If a log group returned zero errors, say so in scan_notes.`,
    `- Container Insights / control-plane logging may be off; "no log group" or "empty" is a finding, not a failure.`,
    `- Insights has a 15-min query ceiling; if a query times out, shrink the window and note it.`,
    ``,
    `Return ONLY the structured object. sample_message verbatim, counts from statistics, no invented numbers.`,
  ].join('\n')
}

function enrichPrompt(svc, unmatched) {
  return [
    `You are enriching UNMATCHED error signatures for service "${svc.name}" — errors that matched no known`,
    `pattern in error-patterns.yaml. For each, find the likely cause from authoritative AWS docs.`,
    ``,
    `Unmatched errors (with one verbatim sample each):`,
    ...unmatched.map((f, i) => `${i + 1}. [${f.severity}] ${f.error_signature}\n   sample: ${f.sample_message}`),
    ``,
    `For each error:`,
    `- Use the aws-knowledge MCP (find it via ToolSearch: tool \`mcp__aws-knowledge__aws___search_documentation\`,`,
    `  then \`...read_documentation\` on the best hit) to search the symptom/error string.`,
    `- If the search surfaces an SOP, note it. Propose a cause grounded in what the docs say.`,
    `- Cite the doc URLs / SOP names you actually used in \`sources\`.`,
    ``,
    `Honesty rules:`,
    `- If MCP returns nothing relevant, set proposed_cause to say so explicitly and confidence "low". Do NOT fabricate.`,
    `- Never state AWS-specific numbers (limits, quotas, timeouts) from memory — only from the docs you read.`,
    ``,
    `Return ONLY the structured object, one entry per unmatched error.`,
  ].join('\n')
}

// ── Fan-out: pipeline, no barrier. Each service scans, then (if it has any
//    unmatched findings) enriches — independently of the other services. ──
phase('Scan')
log(`Scanning ${SERVICES.length} service(s) in ${ACCOUNT}/${REGION}, last ${HOURS}h`)

const results = await pipeline(
  SERVICES,
  // Stage 1 — scan + pattern-match (needs Bash + Read; general-purpose has them)
  (svc) => agent(scanPrompt(svc), {
    label: `scan:${svc.name}`,
    phase: 'Scan',
    schema: SCAN_SCHEMA,
    agentType: 'general-purpose',
  }),
  // Stage 2 — enrich only the unmatched findings, via aws-knowledge MCP
  (scan, svc) => {
    if (!scan) return null
    const unmatched = (scan.findings || []).filter(f => !f.matched_pattern_id)
    if (!unmatched.length) return scan
    return agent(enrichPrompt(svc, unmatched), {
      label: `enrich:${svc.name}`,
      phase: 'Enrich',
      schema: ENRICH_SCHEMA,
      agentType: 'general-purpose',
    }).then(enr => ({ ...scan, enrichment: enr }))
      .catch(() => ({ ...scan, enrichment: null, scan_notes: (scan.scan_notes || '') + ' [enrich stage failed]' }))
  }
)

const services = results.filter(Boolean)
const totalFindings = services.reduce((n, s) => n + ((s.findings || []).length), 0)
log(`Done: ${services.length}/${SERVICES.length} service(s), ${totalFindings} finding(s) total`)

return {
  scope: { account_id: ACCOUNT, region: REGION, hours_back: HOURS, services: SERVICES.map(s => s.name) },
  services,
}
