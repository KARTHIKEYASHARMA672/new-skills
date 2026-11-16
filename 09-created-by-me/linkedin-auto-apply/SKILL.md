---
name: linkedin-auto-apply
description: "Autonomous LinkedIn Easy Apply execution engine. Methodically searches, filters, fills multi-step application modals, attaches verified resumes, enforces strict compensation & graduation constraints, appends submission timestamp records into Excel/CSV trackers without file recreation, and pushes updates to GitHub memory."
metadata:
  icon: work
  author: A. Praneeth Karthikeya Sharma
  version: 2.0.0
  category: business-social
---

# 🚀 LinkedIn Auto-Apply Skill

An enterprise-grade, autonomous job application engine designed to maximize LinkedIn job search yield while adhering strictly to LinkedIn platform limits, anti-bot safeguards, and candidate profile integrity.

---

## 📌 1. Operational Overview & Platform Rules

LinkedIn enforces an account-level rolling daily cap of **30 to 40 Easy Apply submissions per 24 hours** (typically capping around ~35 applications). When the limit is reached, LinkedIn displays:
> *"You reached today's Easy Apply limit. Great effort applying today. We limit Easy Apply submissions to help ensure each application gets the right attention. Save this job and continue applying tomorrow."*

### Key Operating Directives:
1. **Never Flood or Rapid-Fire:** Maintain a strict **15 to 30 second delay** between job applications to protect account reputation and prevent rate limiting.
2. **Never Regenerate Files from Scratch:** Always use **in-place row appending** via `append_job_application.py` to record applications by date and exact submission time (`HH:MM:SS IST`).
3. **Capture Proof:** Save confirmation screenshots immediately upon application submission into `screenshots/`.
4. **Immediate Graceful Stop:** When LinkedIn triggers the daily limit modal, cleanly stop and sync all completed records without corrupted retries.

---

## 🎯 2. The 8-Role Priority & Daily Allocation Matrix (35 Applications / Day)

Daily applications are distributed proportionally across the user's **8 preferred AI roles**:
$$\frac{35 \text{ daily limit}}{8 \text{ roles}} = 4 \text{ applications base} + 3 \text{ remainder allocated to top 3 priorities}$$

| Priority | Role Category / Target Title | Daily Quota | Search Queries & Keywords | Core Tech Stack |
| :---: | :--- | :---: | :--- | :--- |
| **#1** | **Generative AI Solution Developer** | **5 Jobs** | `"Generative AI Developer"`, `"GenAI Solutions"`, `"LLM Engineer"` | Python, LLMs, RAG, FastAPI, Vector DBs, Prompt Design |
| **#2** | **Agentic AI Specialist / AI Agent Builder** | **5 Jobs** | `"Agentic AI"`, `"AI Agent Builder"`, `"Autonomous Agents"` | LangGraph, CrewAI, AutoGen, Multi-Agent Protocols |
| **#3** | **AI Product Prototyper / AI Builder** | **5 Jobs** | `"AI Product Prototyper"`, `"AI Builder"`, `"Full-Stack AI"` | Rapid Prototyping, Next.js, React 19, Generative UI, APIs |
| **#4** | **AI Solution & Implementation Associate** | **4 Jobs** | `"AI Solutions Associate"`, `"AI Implementation Specialist"` | Enterprise AI Solutions, Model Integration, Deployment |
| **#5** | **AI Workflow & Automation Specialist** | **4 Jobs** | `"AI Workflow Automation"`, `"AI Automation Engineer"` | n8n, LangChain, Workflow Orchestration, Python Pipelines |
| **#6** | **AI Content & Operations Specialist** | **4 Jobs** | `"AI Content Operations"`, `"AI Operations Specialist"` | Synthetic Data, Model Evaluation, GTM Ops, Tracing |
| **#7** | **Prompt Engineering** | **4 Jobs** | `"Prompt Engineer"`, `"Prompt Design"`, `"Prompt Architect"` | Few-Shot Prompting, Evaluation Rubrics, System Prompts |
| **#8** | **Smart System & IoT Automation Tester** | **4 Jobs** | `"IoT Automation Tester"`, `"Smart Systems QA"`, `"Embedded AI"` | Raspberry Pi, Sensor Fusion, Edge AI, Hardware QA |
| **TOTAL** | **8 Focused Roles Across All AI Domains** | **35 Jobs** | **Daily Rolling Allocation (5 + 5 + 5 + 4 + 4 + 4 + 4 + 4 = 35)** | Full AI Lifecycle Coverage |

---

## 👤 3. Candidate Profile Rules (Mandatory & Non-Negotiable)

Every questionnaire, form field, and application modal must strictly use the following candidate parameters:

| Field | Required Value | Notes & Enforcement |
| :--- | :--- | :--- |
| **Full Name** | A. Praneeth Karthikeya Sharma | First: `Praneeth Karthikeya`, Last: `Sharma` |
| **Email** | `karthikeyasharma672@gmail.com` | Primary contact email |
| **Phone** | `+91 949 262 3987` | Country Code: India (`+91`) |
| **Degree / Education** | B.Tech in ECE (IoT), Lovely Professional University | 2023–2027 |
| **Graduation Year** | **2027** | 🚨 **NEVER ENTER 2026.** Must strictly be 2027. |
| **Notice Period / Availability** | **0 days / Immediate** | Relieved student status; immediately available. |
| **Relevant Experience** | **1 year** | Applied for Python, AI, LLMs, Agents, Full-Stack, IoT. |
| **Foreign Remote Compensation** | **6 LPA** | ₹6,00,000 INR/yr, or \$10,000–\$15,000 USD/yr, or \$60–\$120/hr contract. |
| **Indian Role Compensation** | **10 LPA+** | ₹10,00,000 INR/yr or up to posted range (e.g. 30–45 LPA). |
| **Attached Resume** | `Praneeth_Karthikeya_Sharma_Resume_Updated.pdf` | Strict 2-page PDF with 6 ranked GitHub projects. |

---

## 🔍 4. LinkedIn Search & Application Execution Workflow

### Step 0: Browser Initialization & Direct One-Step Entry
1. Open the built-in browser in Antigravity.
2. On the default Google interface start page, search for **LinkedIn** and click the top result (or navigate directly to `https://www.linkedin.com/in/karthikeya-sharma672/`).
3. This immediately opens the user's authenticated LinkedIn profile/feed with zero login prompts or security barriers.
4. From there, navigate directly to **LinkedIn Jobs** (`https://www.linkedin.com/jobs/`).

### Step 1: Search & Filter Setup
Navigate to `https://www.linkedin.com/jobs/` and apply the search parameters:
- **Easy Apply:** `f_AL=true`
- **Date Posted:** Past 24 hours (`f_TPR=r86400`)
- **Location:** `India` (Remote, Hybrid, On-site) or `Worldwide` (Remote)
- **Sort By:** Most recent (`sortBy=DD`)

### Step 2: Modal Navigation & Questionnaire Answering
1. Click **Easy Apply**.
2. **Contact Info Screen:** Verify Name, Phone, Email, Location (`Hyderabad` / `Bengaluru` / `Remote`).
3. **Resume Screen:** Select or upload `Praneeth_Karthikeya_Sharma_Resume_Updated.pdf`.
4. **Additional Questions Screen:**
   - *Experience Questions:* Enter `1` for relevant skills.
   - *Graduation / Year:* Enter `2027`.
   - *Notice Period:* Enter `0` or `Immediate`.
   - *Expected Salary:* Enter `600000` (Foreign Remote) or `1000000` (India).
   - *Yes/No Questions:* Answer affirmatively (`Yes`) for legal authorization, remote suitability, and willingness to learn/relocate.
5. **Review Screen:** Verify answers and click **Submit Application**.
6. **Capture Confirmation Screenshot:** Save step evidence to `screenshots/`.
7. **Pacing Delay:** Wait 15–30 seconds before opening the next job card.

---

## 📊 5. In-Place Tracker Updating (`append_job_application.py`)

Do not regenerate or overwrite the Excel workbook. Use the modular script:

```bash
python "L:\linkedin job search\append_job_application.py" \
  --role-cat "Role 1: GenAI Solutions Developer" \
  --company "Company Name" \
  --role "Job Title" \
  --type-loc "Remote (India)" \
  --date-posted "Today (< 2 hrs)" \
  --status "Applied (Easy Apply)" \
  --skills "Python, LLMs, LangGraph" \
  --details "Expected CTC: 10 LPA | Notice: 0 days | Grad: 2027" \
  --resume "Praneeth_Karthikeya_Sharma_Resume_Updated.pdf" \
  --url "https://www.linkedin.com/jobs/view/XXXXXX/"
```

### What `append_job_application.py` does:
1. Calculates the next `S.No` automatically from the CSV.
2. Captures current Date (`YYYY-MM-DD`) and exact submission Time (`HH:MM:SS IST`).
3. Appends the record into `LinkedIn_AI_Job_Applications_Tracker.csv`.
4. Uses `openpyxl` to insert a styled row into `LinkedIn_AI_Job_Applications_Tracker.xlsx` at `last_data_row + 1`.
5. Updates the subtitle banner in Row 2 with the updated total count and timestamp.

---

## 🔄 6. Cloud Memory & GitHub Synchronization

After each batch or daily run, sync the CSV to the GitHub repository:
- **Repository:** `KARTHIKEYASHARMA672/memory`
- **File:** `LinkedIn_AI_Job_Applications_Tracker.csv`
- **Method:** `github-mcp-server` tool `create_or_update_file` with branch `main`.

---

## ⏰ 7. Nightly 12:00 AM IST Automation Sidecar

To run autonomously every night at 12:00 AM IST:
- **Sidecar Path:** `~/.gemini/config/sidecars/daily-linkedin-job-apply/sidecar.json`
- **Cron Expression:** `CRON_TZ=Asia/Kolkata 0 0 * * *`
- **Restart Policy:** `always`
- **Workspace:** `file:///L:/linkedin%20job%20search`
