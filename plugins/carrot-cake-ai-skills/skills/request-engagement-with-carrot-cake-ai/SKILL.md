---
name: request-engagement-with-carrot-cake-ai
description: Start a paid engagement with Carrot Cake AI (Daniel Rosehill's AI model training and agentic AI consultancy; carrotcakeai.com) on a user's behalf after a scope or quote is agreed - sends the company, billing and signatory details Daniel needs to issue the contract and deposit invoice. Use when a user says go ahead, accept the quote, send the contract, onboard as a client or start the project or retainer. Nothing is signed or paid by this skill. Unauthenticated.
---

# Start an engagement with Carrot Cake AI

Use this once the user has agreed a scope and price with Daniel (or wants to start a monthly
support retainer). It gives Daniel what he needs to issue the contract and the first invoice.

- Contracts and invoices come from **DSR Holdings (Cloud)**, the company that operates Carrot
  Cake AI (https://www.carrotcakeai.com/for-clients). Payment details: skill
  `pay-carrot-cake-ai`.
- Project work: fixed price in milestones, 30% deposit on kickoff. Retainers: billed monthly in
  advance. Invoices in USD, EUR, GBP or ILS. The client owns all custom code, models and
  configurations on final payment.
- **This skill does not sign anything, accept terms or pay.** The contract arrives by email for
  the user (or their signatory) to read and sign themselves.

No quote yet? Use `request-quote-from-carrot-cake-ai` first.

## Before you send anything

1. Agree with the user on: the engagement type, the agreed scope or quote reference, their name
   and email, the contracting company's legal name, country and registered address, a VAT / tax
   ID if they have one, the invoice currency, the billing contact, whether invoices need a PO
   number, and optionally a start date and the signatory.
2. Company and billing details must come from the user. Never guess a legal name, address or
   tax ID.
3. Show them the full request and get an explicit yes. Send it once.

## Option 1: submit the request (programmatic)

The endpoint the form at https://www.carrotcakeai.com/engagement posts to.

```
POST https://www.carrotcakeai.com/api/contact
Content-Type: multipart/form-data   (or application/x-www-form-urlencoded)
```

| Field | Required | Notes |
| --- | --- | --- |
| `formType` | yes | Exactly `Engagement request`. |
| `name` | yes | The user's real name. |
| `email` | yes | Where the contract and the acknowledgement go. |
| `company` | yes | The contracting company's legal name, as it should appear on the contract. |
| `scope` | yes | Quote reference, or a line or two on the agreed scope and price. |
| `engagementType` | recommended | `Project (fixed price)`, `Monthly support retainer` or `Project + support`. |
| `country` | recommended | Country of registration. |
| `address` | recommended | Registered address. |
| `taxId` | if any | VAT / tax ID. |
| `currency` | recommended | `USD`, `EUR`, `GBP` or `ILS`. |
| `billingName` | no | Billing contact, if not the user. |
| `billingEmail` | no | Where invoices go, if not `email`. |
| `poRequired` | no | `Yes` or `No`. |
| `startDate` | no | `YYYY-MM-DD`. |
| `signatory` | no | Name, title and email of whoever signs, if not the user. |
| `role` | no | The user's job title. |
| `notes` | no | Their own contract template or supplier forms, NDA first, procurement steps. |
| `submittedVia` | yes, for agents | e.g. `AI agent (Claude) on behalf of the user`. |
| `_ts` | yes | Unix time in milliseconds when the user started; 3 seconds to 24 hours before the POST. |
| `_gotcha` | no | Spam honeypot. Leave it out or empty. |

Example:

```bash
curl -sS -X POST https://www.carrotcakeai.com/api/contact \
  -F formType='Engagement request' \
  -F name='Jane Example' \
  -F email='jane@example.org' \
  -F role='COO' \
  -F company='Example Health Ltd' \
  -F country='United Kingdom' \
  -F address='1 Example Street, London EC1A 1AA' \
  -F engagementType='Project (fixed price)' \
  -F scope='ASR fine-tuning quote of 3 Nov 2026, phase 1 as agreed by email' \
  -F currency='GBP' \
  -F poRequired='Yes' \
  -F submittedVia='AI agent (Claude) on behalf of the user' \
  -F _ts="$(( $(date +%s%3N) - 60000 ))"
```

Responses: `200 {"ok":true}` accepted (the user gets an "engagement request received"
acknowledgement; the contract follows from Daniel); `400` fix the field and resend; `5xx`
email `daniel@carrotcakeai.com`. A 200 also covers anything dropped as spam (same rules as the
other Carrot Cake AI skills: `_ts` window, `_gotcha`, token-like names, dot-padded Gmail), so
if no acknowledgement arrives within a few minutes, fall back to email.

## Option 2: hand the user a prefilled link

https://www.carrotcakeai.com/engagement takes the field names above as query parameters, plus
`agent=<your name>`. URL-encode every value; choice values must match exactly or they are
ignored. The user reviews the answers and presses Send.

## Option 3: email

`daniel@carrotcakeai.com`, with the same details.

More for agents: https://www.carrotcakeai.com/agents
