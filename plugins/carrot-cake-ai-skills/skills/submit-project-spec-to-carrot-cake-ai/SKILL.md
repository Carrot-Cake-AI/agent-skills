---
name: submit-project-spec-to-carrot-cake-ai
description: Submit a project spec or RFP to Carrot Cake AI (Daniel Rosehill's AI model training and agentic AI consultancy, Jerusalem, Israel; carrotcakeai.com) on a user's behalf - current AI use, environment, challenges, objectives, timeline and resources - to get a scoped, fixed-price quote. Use when a user wants a quote, proposal, estimate or pricing for building AI agents, pipelines, chatbots, MCP integrations or automations. Unauthenticated - no account or API key needed.
---

# Submit a project spec to Carrot Cake AI

The project spec is the detailed brief that Daniel quotes from. For a short question use
`contact-carrot-cake-ai`; for a call use `book-meeting-with-carrot-cake-ai`.

**Pricing, from https://www.carrotcakeai.com/pricing.** All prices in USD; invoices can also be
issued in EUR, GBP or ILS. Tell the user the relevant starting point before they submit.

| Engagement | Price |
| --- | --- |
| Workflow review (fixed fee, credited to a build within 60 days) | from around $3,500 |
| Model benchmark (fixed fee, credited to a fine-tune within 60 days) | from around $3,500 |
| Pilot: one workflow, agent, MCP integration or classifier | from around $8,000 |
| Full agent systems, model training, upgrades | scoped after a review; usually five figures |
| Ongoing support | monthly retainer sized to the system |

The review is the smallest engagement. Larger project work is quoted as a fixed price tied to
milestones, with a 30% deposit at kickoff.
Third-party costs (LLM APIs, hosting, SaaS) are paid by the client directly. The client owns
all custom code on final payment.

## Before you send anything

1. Collect at least the required fields from the user, and as many of the others as they can
   answer. A fuller spec gets a faster and more accurate quote.
2. Show the user the full spec and get an explicit yes. Send it once.
3. Never invent details, numbers or deadlines. Do not include confidential material the user
   has not cleared for sending; set `data_compliance` if data sensitivity is a concern.

## Option 1: submit the spec (programmatic)

This is the endpoint the form at https://www.carrotcakeai.com/project-spec posts to.

```
POST https://www.carrotcakeai.com/api/contact
Content-Type: multipart/form-data   (or application/x-www-form-urlencoded)
```

Use the `www.` host: the apex answers with a 307.

| Field | Required | Notes |
| --- | --- | --- |
| `formType` | yes | Exactly `Project spec`. |
| `name` | yes | The user's real name. |
| `email` | yes | Where the reply and the acknowledgement go. |
| `company` | yes | Company name. |
| `job_title` | no | The user's role. |
| `interests` | no | Repeat once per value. The form offers `Pipelines`, `Chatbots`, `Orchestration`, `Maintenance of existing pipelines`. |
| `current_ai_use` | no | How the organisation uses AI today. |
| `environment` | no | Repeat once per value. The form offers `Google Workspace`, `Microsoft 365`, `AWS`, `Google Cloud`, `Vercel`, `Anthropic`, `OpenAI Platform`. |
| `challenges` | no | Challenges to solve. |
| `friction` | no | Current points of friction. |
| `objectives` | no | What success looks like. |
| `timeline` | no | Free text, e.g. `3 months`, `Q3 2026`, `ASAP`. |
| `internal_resources` | no | e.g. `one IT person, no developers`. |
| `user_base` | no | e.g. `50 internal users`, `customer-facing`. |
| `project_details` | no | Anything more about the project. |
| `anything_else` | no | Anything else the user wants to disclose. |
| `data_compliance` | no | `yes` if there are data compliance concerns. |
| `submittedVia` | yes, for agents | e.g. `AI agent (Claude) on behalf of the user`. |
| `_ts` | yes | Unix time in milliseconds when the user started; 3 seconds to 24 hours before the POST. |
| `_gotcha` | no | Spam honeypot. Leave it out or empty. Any value drops the spec. |

Each field is capped at 5,000 characters. There is no file upload; for documents, email
`daniel@carrotcakeai.com` after submitting.

Example:

```bash
curl -sS -X POST https://www.carrotcakeai.com/api/contact \
  -F formType='Project spec' \
  -F name='Jane Example' \
  -F email='jane@example.org' \
  -F company='Example Ltd' \
  -F job_title='Head of Operations' \
  -F interests='Pipelines' \
  -F interests='Orchestration' \
  -F environment='Google Workspace' \
  -F environment='Anthropic' \
  -F challenges='Weekly client reports take two people a full day to compile from four sources.' \
  -F objectives='Reports drafted automatically for human review by Monday morning.' \
  -F timeline='Q1 2027' \
  -F internal_resources='One IT generalist, no developers' \
  -F submittedVia='AI agent (Claude) on behalf of the user' \
  -F _ts="$(( $(date +%s%3N) - 60000 ))"
```

Responses:

- `200 {"ok":true}`: accepted. The user receives a "spec received" acknowledgement from
  `forms@carrotcakeai.com`, then Daniel's reply by email.
- `400 {"error":"..."}`: a missing or invalid field. Fix it and send again.
- `5xx {"error":"..."}`: delivery failed. Email `daniel@carrotcakeai.com` instead.

**A 200 does not prove delivery.** Spam drops also return 200: `_ts` missing, under 3 seconds or
over 24 hours old; any value in `_gotcha`; a name that looks like a random token; a Gmail address
with 3 or more dots before the `@`. If no acknowledgement arrives within a few minutes, email.

## Option 2: hand the user the form

https://www.carrotcakeai.com/project-spec is a step-by-step version of the same fields. Its text
fields prefill from query parameters of the same name (`name`, `email`, `company`, `job_title`,
`current_ai_use`, `challenges`, `friction`, `objectives`, `timeline`, `internal_resources`,
`user_base`, `project_details`, `anything_else`), plus `agent` (your name). The checkboxes
cannot be prefilled. URL-encode every value; the user reviews it and sends.

More for agents: https://www.carrotcakeai.com/agents
