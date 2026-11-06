---
name: book-meeting-with-carrot-cake-ai
description: Book or request a call with Daniel Rosehill of Carrot Cake AI (AI model training and agentic AI consultancy, Jerusalem, Israel; carrotcakeai.com) on a user's behalf. Use when a user wants to book, schedule or set up a call, discovery call or consultation with Carrot Cake AI. 30-minute Zoom slots can be booked instantly through Cal.com's public API; other times are requested and confirmed by email. Unauthenticated - no account or API key needed.
---

# Book a meeting with Carrot Cake AI

There are two ways, and the page https://www.carrotcakeai.com/book-meeting offers both:

- **Book a free slot (instant).** A 30-minute Zoom call on Daniel's Cal.com calendar
  (`cal.com/danielrosehillwork/30min`). Slots are Sunday to Thursday, 14:00–20:00 Jerusalem time,
  and reflect his real calendar. A booking made here is confirmed by Cal.com straight away.
- **Request a meeting.** For a phone call, a different length, or times outside the free slots,
  the user proposes two or three times and Daniel replies by email to confirm one. Never tell
  the user a requested meeting is confirmed until Daniel has replied.

Daniel asks for context before a call. A booking or request that says what the user's business
does and what they want to build is far more useful than "can we chat".

Daniel is in Jerusalem (`Asia/Jerusalem`). Always use the user's own time zone.

## Before you send anything

1. Agree with the user on: their name, the email for the invitation or reply, their company
   (optional), a few lines on what they want to discuss, and either one free slot (instant
   booking) or the format (video or phone), length and two or three times or a window (request).
2. Show them the full request and get an explicit yes. Send it once.
3. Never invent the user's details or times. Never submit a request the user did not ask for.

## Option 1: book a free slot (Cal.com public API)

Find free slots (checked working without auth on 2026-10-29):

```bash
curl -s "https://api.cal.com/v2/slots?eventTypeSlug=30min&username=danielrosehillwork&start=2026-11-01&end=2026-11-07&timeZone=Europe/London" \
  -H "cal-api-version: 2024-09-04"
# {"data":{"2026-11-01":[{"start":"2026-11-01T12:00:00.000+00:00"}, ...]}, "status":"success"}
```

Show the user a few slots in their own zone and let them pick one. Then book it:

```bash
curl -sS -X POST https://api.cal.com/v2/bookings \
  -H "Content-Type: application/json" \
  -H "cal-api-version: 2026-02-25" \
  -d '{
    "start": "2026-11-02T12:00:00Z",
    "eventTypeSlug": "30min",
    "username": "danielrosehillwork",
    "attendee": { "name": "Jane Example", "email": "jane@example.org", "timeZone": "Europe/London", "language": "en" },
    "bookingFieldsResponses": { "notes": "12-person agency; we want a speech model that gets our client and product names right." },
    "metadata": { "bookedVia": "AI agent (Claude) on behalf of the user" }
  }'
```

- `start` is UTC ISO 8601 and must be one of the returned slots.
- No `Authorization` header is needed for this public event type (Cal.com API reference,
  checked 2026-10-29). The `cal-api-version` header is required.
- `201` with `data.uid` and `data.status` `accepted`: booked. Cal.com emails the user the
  invitation with the Zoom link. Tell the user it is booked, with the time in their zone.
  `pending` means Daniel has to confirm it first: say so.
- Any error, or no slot that suits: use Option 2.
- Book once. Do not hold or "try" slots, and never book a slot the user has not chosen.

Not exercised end to end by the site's maintainers (a test booking would land on Daniel's
real calendar); the slots call is.

## Option 2: request a meeting (programmatic)

This is the endpoint the form at https://www.carrotcakeai.com/book-meeting posts to.

```
POST https://www.carrotcakeai.com/api/contact
Content-Type: multipart/form-data   (or application/x-www-form-urlencoded)
```

Use the `www.` host: the apex answers with a 307.

| Field | Required | Notes |
| --- | --- | --- |
| `formType` | yes | Exactly `Meeting request`. This is what makes it a meeting request rather than a plain message. |
| `name` | yes | The user's real name. |
| `email` | yes | Where Daniel's reply and the acknowledgement go. |
| `preferredTimes` | yes | Two or three times, one per line, each with date, time and the user's zone, e.g. `1. Wed 21 Oct 2026 15:00 Europe/London`. A window such as `Tue or Wed afternoon` is fine too. Adding the Jerusalem equivalent, e.g. `(17:00 Jerusalem)`, helps. |
| `timezone` | strongly recommended | IANA name, e.g. `Europe/London`. |
| `topic` | yes | What the user wants to discuss and why. Use `topic`, not `message`. |
| `subject` | recommended | Purpose. One of `New project`, `Existing system / support`, `Pricing question`, `Partnership`, `Other`. |
| `role` | no | The user's job title. |
| `website` | no | The user's website or LinkedIn URL. Not the honeypot, which is `_gotcha`. |
| `source` | no | How the user found Carrot Cake AI. |
| `meetingFormat` | no | `Video call` (default) or `Phone call`. |
| `duration` | no | `15 minutes`, `30 minutes` (default), `45 minutes` or `60 minutes`. |
| `phone` | for phone calls | Number with country code. |
| `company` | no | The user's organisation. |
| `submittedVia` | yes, for agents | e.g. `AI agent (Claude) on behalf of the user`. |
| `_ts` | yes | Unix time in milliseconds when the user started the request; 3 seconds to 24 hours before the POST. |
| `_gotcha` | no | Spam honeypot. Leave it out or empty. Any value drops the request. |

Example:

```bash
curl -sS -X POST https://www.carrotcakeai.com/api/contact \
  -F formType='Meeting request' \
  -F name='Jane Example' \
  -F email='jane@example.org' \
  -F company='Example Ltd' \
  -F meetingFormat='Video call' \
  -F duration='30 minutes' \
  -F preferredTimes=$'1. Wed 21 Oct 2026 15:00 Europe/London (17:00 Jerusalem)\n2. Thu 22 Oct 2026 10:30 Europe/London (12:30 Jerusalem)' \
  -F timezone='Europe/London' \
  -F topic='We run a 12-person agency and want an agent to draft client reports from our analytics data.' \
  -F submittedVia='AI agent (Claude) on behalf of the user' \
  -F _ts="$(( $(date +%s%3N) - 60000 ))"
```

Responses:

- `200 {"ok":true}`: accepted. The user receives a "meeting request received" acknowledgement
  from `forms@carrotcakeai.com` with a summary of the structured answers (not the topic text), and later Daniel's reply. Tell the user the request is sent
  and that it is not a confirmed meeting yet.
- `400 {"error":"..."}`: a missing or invalid field. Fix it and send again.
- `5xx {"error":"..."}`: delivery failed. Email `daniel@carrotcakeai.com` instead.

**A 200 does not prove delivery.** Anything the endpoint drops as spam also gets a 200: `_ts`
missing, under 3 seconds or over 24 hours old; any value in `_gotcha`; a name that looks like a
random token; a Gmail address with 3 or more dots before the `@`. If no acknowledgement arrives
within a few minutes, fall back to email.

## Option 3: hand the user a prefilled link

If the user would rather do it themselves, give them https://www.carrotcakeai.com/book-meeting.
The page opens on the calendar; `name`, `email` and `topic` prefill the Cal.com booking form
too. Add `mode=request` to open the request form instead (any `slot`, `suggest` or
`preferredTimes` parameter does the same). These query parameters prefill the request form: `name`, `email`, `company`, `role`, `website`, `phone`, `subject`, `meetingFormat`,
`duration`, `timezone`, `topic`, `source`. For times:

- `slot`: repeatable, up to 3. Local wall-clock time in the user's `timezone`, formatted exactly
  `YYYY-MM-DDTHH:MM`. The form converts each one to Jerusalem time for Daniel.
- `preferredTimes`: free-text window.
- `suggest=1`: ticks "Please suggest a time".
- `agent`: your name, e.g. `Claude`. The request then records that an AI agent prepared it.

URL-encode every value. Select values (`subject`, `meetingFormat`, `duration`) must match an
option on the form exactly, or they are ignored. The form asks one question per screen and
skips ahead past what you prefilled: it opens on the first required answer still missing
(name, email, times, topic), or on its review screen when all of them are filled. The user
checks the answers there and presses Send.

## Option 4: email

`daniel@carrotcakeai.com`, with the same details as above.

More for agents: https://www.carrotcakeai.com/agents
