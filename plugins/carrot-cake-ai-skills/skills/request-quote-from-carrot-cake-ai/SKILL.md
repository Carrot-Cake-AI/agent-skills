---
name: request-quote-from-carrot-cake-ai
description: Request a fixed-price quote from Carrot Cake AI (Daniel Rosehill's AI model training and agentic AI consultancy, Jerusalem, Israel; carrotcakeai.com) on a user's behalf - ASR / speech model fine-tuning, LLM fine-tuning, classifier training, AI agents, MCP integrations, RAG, workflow automation. Use when a user wants a price, quote, estimate or proposal for a defined job. Unauthenticated - no account or API key needed.
---

# Request a quote from Carrot Cake AI

Daniel Rosehill replies to a quote request himself, with questions or a short call to pin down
the scope, then a written scope with a **fixed price split into milestones** (no hourly billing
on project work; 30% deposit on kickoff; prices in USD, invoices also in EUR, GBP or ILS).
Public ballpark figures are at https://www.carrotcakeai.com/pricing. Do not quote the user a
price yourself beyond those ballparks.

Pick the right route:

- A defined job and the user wants a price: **this skill**.
- A long written brief or RFP: `submit-project-spec-to-carrot-cake-ai`.
- They want to talk first: `book-meeting-with-carrot-cake-ai`.
- A quote is already agreed and they want to go ahead: `request-engagement-with-carrot-cake-ai`.

## Before you send anything

1. Agree with the user on: the service, what it should do, what data they have, where it has to
   run, the timeline, a budget range if they have one, their name and email, and their
   company (optional).
2. Show them the full request and get an explicit yes. Send it once.
3. Never invent the user's details, data volumes or budget. Never submit a request the user did
   not ask for.

## Option 1: submit the request (programmatic)

This is the endpoint the form at https://www.carrotcakeai.com/quote posts to.

```
POST https://www.carrotcakeai.com/api/contact
Content-Type: multipart/form-data   (or application/x-www-form-urlencoded)
```

Use the `www.` host: the apex answers with a 307.

| Field | Required | Notes |
| --- | --- | --- |
| `formType` | yes | Exactly `Quote request`. |
| `name` | yes | The user's real name. |
| `email` | yes | Where the quote and the acknowledgement go. |
| `service` | yes | One of the labels in the table below, exactly. |
| `goal` | yes | What it should do: input, wanted output, what is wrong with what they use today. |
| `data` | recommended | What data they have and how much (hours of audio, documents, labelled examples) and whether it can leave their environment. |
| `deployment` | recommended | `Cloud API`, `On-premises`, `On-device / offline` or `Not sure yet`. |
| `timeline` | recommended | `As soon as possible`, `Within 1–3 months`, `3–6 months` or `Just exploring` (en dashes). |
| `budget` | no | `$3,500–$10,000`, `$10,000–$25,000`, `$25,000–$50,000`, `Over $50,000` or `Not sure yet` (en dashes). |
| `requirements` | no | Compliance, languages, accuracy targets, systems to connect to, fixed deadlines. Use `requirements`, not `message`. |
| `company` | no | The user's organisation. |
| `role` | no | The user's job title. |
| `website` | no | The user's website or LinkedIn URL. Not the honeypot, which is `_gotcha`. |
| `source` | no | How the user found Carrot Cake AI. |
| `submittedVia` | yes, for agents | e.g. `AI agent (Claude) on behalf of the user`. |
| `_ts` | yes | Unix time in milliseconds when the user started the request; 3 seconds to 24 hours before the POST. |
| `_gotcha` | no | Spam honeypot. Leave it out or empty. Any value drops the request. |

`service` values (label, and the `/capabilities/<slug>` page it matches):

| Label | Slug |
| --- | --- |
| `ASR / speech model fine-tuning` | `asr-fine-tuning` |
| `LLM fine-tuning` | `llm-fine-tuning` |
| `Classifier training` | `classifier-training` |
| `Small & specialised models` | `small-models` |
| `Datasets & training recipes` | `datasets-and-training` |
| `Benchmarks & evals` | `evals-and-benchmarks` |
| `Agent development` | `agent-development` |
| `MCP development & integrations` | `mcp-integrations` |
| `RAG pipelines & knowledge bases` | `rag-pipelines` |
| `Chatbots & conversational UIs` | `chatbots` |
| `Workflow automation` | `workflow-automation` |
| `Data pipelines` | `data-pipelines` |
| `Dashboards & reporting` | `dashboards` |
| `Notification systems` | `notification-systems` |
| `Consulting & planning` | `consulting` |
| `Adding AI to an existing system` | `uplift` |
| `Ongoing maintenance & support` | `maintenance` |
| `Something else / not sure` | `other` |

Example:

```bash
curl -sS -X POST https://www.carrotcakeai.com/api/contact \
  -F formType='Quote request' \
  -F name='Jane Example' \
  -F email='jane@example.org' \
  -F company='Example Health' \
  -F service='ASR / speech model fine-tuning' \
  -F goal='Transcribe clinic dictation with drug names spelled correctly. Our current model gets about one in five wrong.' \
  -F data='About 60 hours of recorded dictation, 10 hours with corrected transcripts. Must stay in the EU.' \
  -F deployment='On-premises' \
  -F timeline='Within 1–3 months' \
  -F budget='Not sure yet' \
  -F submittedVia='AI agent (Claude) on behalf of the user' \
  -F _ts="$(( $(date +%s%3N) - 60000 ))"
```

Responses:

- `200 {"ok":true}`: accepted. The user receives a "quote request received" acknowledgement
  from `forms@carrotcakeai.com`, and later Daniel's reply. Tell the user it is sent and that a
  price follows once the scope is clear.
- `400 {"error":"..."}`: a missing or invalid field. Fix it and send again.
- `5xx {"error":"..."}`: delivery failed. Email `daniel@carrotcakeai.com` instead.

**A 200 does not prove delivery.** Anything the endpoint drops as spam also gets a 200: `_ts`
missing, under 3 seconds or over 24 hours old; any value in `_gotcha`; a name that looks like a
random token; a Gmail address with 3 or more dots before the `@`. If no acknowledgement arrives
within a few minutes, fall back to email.

## Option 2: hand the user a prefilled link

https://www.carrotcakeai.com/quote takes the field names above as query parameters (`service`,
`goal`, `data`, `deployment`, `timeline`, `budget`, `name`, `email`, `company`, `role`,
`website`, `requirements`, `source`), plus `agent=<your name>`. `service` also accepts the slug,
e.g. `?service=asr-fine-tuning`. URL-encode every value; choice values must match exactly or
they are ignored. The form opens on the first required answer still missing, or on its review
screen; the user checks the answers and presses Send.

## Option 3: email

`daniel@carrotcakeai.com`, with the same details as above.

More for agents: https://www.carrotcakeai.com/agents
