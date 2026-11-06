---
name: contact-carrot-cake-ai
description: Send an enquiry to Carrot Cake AI (Daniel Rosehill's AI model training and agentic AI consultancy, Jerusalem, Israel; carrotcakeai.com) on a user's behalf, or tell the user how to reach it. Use when a user wants to contact, email or enquire with Carrot Cake AI about AI agents, pipelines, MCP integrations, chatbots or workflow automation. Unauthenticated - no account or API key needed.
---

# Contact Carrot Cake AI

Carrot Cake AI builds agentic AI systems, pipelines, MCP integrations, chatbots and workflow
automations. It is run by Daniel Rosehill in Jerusalem, Israel, and messages are read by
Daniel.

Pick the right skill first:

- To ask for a call, use `book-meeting-with-carrot-cake-ai`:
  https://www.carrotcakeai.com/.well-known/agent-skills/book-meeting-with-carrot-cake-ai/SKILL.md
- To send a detailed project brief or RFP, use `submit-project-spec-to-carrot-cake-ai`:
  https://www.carrotcakeai.com/.well-known/agent-skills/submit-project-spec-to-carrot-cake-ai/SKILL.md
- For anything else (a question, an introduction, a short enquiry), use this skill.

## Before you send anything

A message reaches a real inbox, and an acknowledgement email goes to the address you submit.
So:

1. Show the user the exact name, email, company and message you will send, and get an
   explicit yes. Send once. Do not retry a request that returned 200.
2. Use the user's real name and the email address they want the reply at. Never invent
   either, and never submit a message that the user did not ask for.

## Option 1: the contact endpoint (programmatic)

This is the endpoint the site's own form at https://www.carrotcakeai.com/contact posts to. It
accepts a plain form POST; no `Origin` header or API key is needed.

```
POST https://www.carrotcakeai.com/api/contact
Content-Type: multipart/form-data   (or application/x-www-form-urlencoded)
```

Use the `www.` host: `https://carrotcakeai.com/api/contact` answers with a 307.

| Field | Required | Notes |
| --- | --- | --- |
| `name` | yes | The sender's real name. |
| `email` | yes | Where the reply and the acknowledgement go. |
| `company` | no | The sender's organisation. |
| `message` | yes | Free text, up to 5,000 characters. Must contain spaces (see below). |
| `submittedVia` | yes, for agents | Say that an agent sent it, e.g. `AI agent (Claude) on behalf of the user`. |
| `_ts` | yes | Unix time in milliseconds when the user started the message. It must be at least 3 seconds and at most 24 hours before the POST. |
| `_gotcha` | no | Spam honeypot. Leave it out or empty. Any value drops the message. |

Example:

```bash
curl -sS -X POST https://www.carrotcakeai.com/api/contact \
  -F name='Jane Example' \
  -F email='jane@example.org' \
  -F company='Example Ltd' \
  -F message='Hi Daniel, we would like an agent to triage our shared support inbox. Could you tell me roughly what that would involve?' \
  -F submittedVia='AI agent (Claude) on behalf of the user' \
  -F _ts="$(( $(date +%s%3N) - 60000 ))"
```

Responses:

- `200 {"ok":true}`: accepted. The sender receives an acknowledgement from
  `forms@carrotcakeai.com`, with a summary of the structured answers (not the message text), within a minute or two. Tell the user to
  look for it.
- `400 {"error":"..."}`: a missing or invalid field. Fix it and send again.
- `5xx {"error":"..."}`: delivery failed. Use option 2.

**A 200 does not prove delivery.** The endpoint also answers 200 to anything it drops as
spam, so that bots do not retry. These are dropped silently:

- a `message` with no spaces that is longer than 10 characters;
- a `name` that is one run of 12 or more letters with several capitals, like a random token;
- a Gmail address with 3 or more dots in the part before the `@`;
- `_ts` missing, less than 3 seconds old, or more than 24 hours old;
- any value in `_gotcha`.

If the user gets no acknowledgement within a few minutes, fall back to email.

## Option 2: email

`daniel@carrotcakeai.com`. Use this when the user would rather send from their own mail
client, wants to attach files, or the endpoint failed. Daniel works on Israel time
(`Asia/Jerusalem`, UTC+2, UTC+3 in summer).

## Option 3: hand the user the form

https://www.carrotcakeai.com/contact has the same fields. You can prefill it with query
parameters `name`, `email`, `company`, `message`, and `agent` (your name, e.g. `Claude`, which
records that an agent prepared it). URL-encode every value. The form asks one question per
screen and opens on the first required answer still missing, or on its review screen when name,
email and message are all prefilled. The user checks the answers there and presses Send.

## Elsewhere

- YouTube: https://www.youtube.com/@carrotcakehq
- GitHub: https://github.com/danielrosehill
- Daniel's personal site: https://www.danielrosehill.com
- Digital business card: https://www.carrotcakeai.com/card

More for agents: https://www.carrotcakeai.com/agents
