---
name: book-editor
description: "Professional book and manuscript editing with track changes and comments. Use when asked to edit books, manuscripts, long-form documents, or any text requiring structural editing, line editing, copy editing, or proofreading. Supports multi-pass workflows for documents too large to edit in a single session. MANDATORY TRIGGERS: edit book, edit manuscript, proofread, copy edit, line edit, structural edit, developmental edit, SPAG check"
---

# Book Editor

Professional editing workflow for manuscripts and long-form documents using Word track changes and comments.

## Overview

Book editing uses docx XML editing to produce proper Word track changes. The author can accept/reject each change in Word.

**Editing process:**
1. Calibration — Edit a small sample, get author feedback, establish preferences
2. Style guide creation — Document decisions for consistency across chunks
3. Multi-pass editing — Work through manuscript in chunks, one pass type at a time
4. Final review — Verify consistency and completeness

## Before Starting

1. Read the technical reference section below for docx XML editing mechanics
2. Create a style guide using template in `references/style-guide-template.md`
3. Confirm with author: chunk size, editing priorities, any style preferences

## Pass Types

Work through the manuscript one pass type at a time, completing all chunks before moving to the next pass.

### Pass 1: Structural/Developmental
Focus: Big picture — chapter organization, argument flow, gaps, redundancies, pacing.

**Output:** Comments only (no track changes). Flag issues for author decision:
- "This section repeats the argument from Chapter 3"
- "Consider moving this earlier to establish context"
- "Gap: the transition from X to Y needs bridging"

### Pass 2: Line Editing
Focus: Paragraph-level clarity — sentence flow, transitions, tightening prose, cutting flab.

**Output:** Track changes for concrete improvements. Comments for questions:
- Track change: Restructure awkward sentences
- Track change: Cut redundant phrases
- Comment: "This paragraph could go two ways — do you want to emphasize X or Y?"

### Pass 3: Copy Editing
Focus: SPAG, consistency, fact-checking, formatting.

**Output:** Primarily track changes. Comments for queries:
- Track change: Spelling, grammar, punctuation fixes
- Track change: Consistency corrections (per style guide)
- Comment: "Please verify this date/name/statistic"

### Pass 4: Final Polish
Focus: Catch anything missed, final read-through.

**Output:** Track changes for remaining issues. Light touch.

## Chunking Strategy

For manuscripts over 5,000 words, work in chunks:

- **Natural boundaries preferred:** Chapters or major sections
- **Fallback chunk size:** 3,000-5,000 words
- **Track progress:** Note which chunks are complete for each pass

**Workflow per chunk:**
1. Unpack docx to XML (see Technical Reference below)
2. Make edits with track changes and comments
3. Pack back to docx
4. Update style guide with any new decisions
5. Move to next chunk

## Style Guide Management

Maintain a running style guide document throughout editing. This ensures consistency across all chunks and passes.

**Create at start:** Copy template from `references/style-guide-template.md`

**Update continuously:** Every spelling choice, terminology decision, or formatting convention goes in the guide. Check guide before each chunk.

**Key categories:**
- Spelling preferences (e.g., "realise" vs "realize")
- Terminology (e.g., "AI" not "A.I.", always "machine learning" not "ML")
- Capitalisation rules (e.g., "Chapter 3" but "the previous chapter")
- Formatting conventions (e.g., how lists appear, heading styles)
- Proper nouns and recurring names
- Numbers (spelled out vs numerals)
- Author voice notes (e.g., "author uses sentence fragments deliberately")

## Track Changes vs Comments

**Use track changes when:**
- The edit is concrete and unambiguous
- You're confident the change improves the text
- SPAG corrections
- Consistency fixes (per style guide)

**Use comments when:**
- Flagging a structural issue for author decision
- The edit could go multiple ways
- Querying facts or requesting clarification
- Explaining why you made a significant change
- Noting a pattern the author should watch for

**Comment style:** Be concise and specific. State the issue and, if relevant, suggest options. Avoid lecturing.

Good: "Unclear antecedent — does 'it' refer to the model or the dataset?"
Bad: "Pronouns should always have clear antecedents. In this sentence, the word 'it' could refer to either..."

## Calibration Phase

Before full editing, calibrate on a sample (1,000-2,000 words):

1. Edit the sample with your default approach
2. Return to author for feedback
3. Adjust based on preferences:
   - Too heavy-handed or too light?
   - Preserving voice appropriately?
   - Right level of comment detail?
   - Any style preferences to add to guide?

This prevents wasted effort if initial instincts don't match author expectations.

## Quality Standards

- **Preserve author voice:** Edit for clarity, not to impose your style
- **Minimal edits:** Don't change what isn't broken
- **Consistency:** Check style guide before each chunk
- **Explain significant changes:** Use comments for non-obvious edits
- **Flag, don't fix, subjective issues:** When reasonable people could disagree, comment rather than change

## Technical Reference: Docx XML Editing

Word `.docx` files are ZIP archives containing XML. To edit with proper track changes:

### Unpack

```bash
mkdir -p work && cp manuscript.docx work/manuscript.zip && cd work && unzip manuscript.zip -d manuscript_xml
```

The key file is `manuscript_xml/word/document.xml` — this contains all body text.

### Track Changes Markup

**Insertions** — wrap new text in a `<w:ins>` element:

```xml
<w:ins w:id="1" w:author="Editor" w:date="2025-01-15T10:00:00Z">
  <w:r w:rsidR="00000001">
    <w:t xml:space="preserve">inserted text </w:t>
  </w:r>
</w:ins>
```

**Deletions** — wrap removed text in a `<w:del>` element:

```xml
<w:del w:id="2" w:author="Editor" w:date="2025-01-15T10:00:00Z">
  <w:r w:rsidDel="00000002">
    <w:delText xml:space="preserve">deleted text </w:delText>
  </w:r>
</w:del>
```

**Replacements** — combine a deletion immediately followed by an insertion at the same location.

Important: Each `w:id` must be unique across the document. Use incrementing integers. The `w:author` and `w:date` attributes control how the change appears in Word's review pane.

### Comments

Comments require entries in two places:

1. **Comment markers in `document.xml`** — mark the commented range:

```xml
<w:commentRangeStart w:id="10"/>
<!-- the commented text runs -->
<w:commentRangeEnd w:id="10"/>
<w:r>
  <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
  <w:commentReference w:id="10"/>
</w:r>
```

2. **Comment content in `word/comments.xml`** — the actual comment text:

```xml
<w:comment w:id="10" w:author="Editor" w:date="2025-01-15T10:00:00Z" w:initials="Ed">
  <w:p>
    <w:r>
      <w:t>Your comment text here.</w:t>
    </w:r>
  </w:p>
</w:comment>
```

If `comments.xml` doesn't exist, create it with the proper namespace declarations and add a relationship entry in `word/_rels/document.xml.rels`:

```xml
<Relationship Id="rIdComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>
```

Also add the content type in `[Content_Types].xml`:

```xml
<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
```

### Repack

```bash
cd manuscript_xml && zip -r ../manuscript_edited.docx . -x ".*" && cd ..
```

The resulting `.docx` will show all changes in Word's Track Changes view.

### Tips

- Always back up the original before editing
- Validate by opening the result in Word/LibreOffice after each chunk
- Preserve all existing XML attributes and namespaces — only modify text content
- When editing `<w:t>` elements, be careful with `xml:space="preserve"` — it controls whitespace handling
