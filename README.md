# Carrot Cake AI: agent skills

The official agent skills for [Carrot Cake AI](https://www.carrotcakeai.com), Daniel
Rosehill's AI model training and agentic AI consultancy in Jerusalem. Each skill is a single
`SKILL.md` in the open [Agent Skills](https://agentskills.io/specification) format, so it works
with any skill-aware agent.

| Skill | What it does |
|---|---|
| `contact-carrot-cake-ai` | Send an enquiry, or find out how to reach Daniel. |
| `book-meeting-with-carrot-cake-ai` | Book a free 30-minute slot, or request another time. |
| `request-quote-from-carrot-cake-ai` | Request a fixed-price quote for a defined job. |
| `submit-project-spec-to-carrot-cake-ai` | Send a project brief or RFP. |
| `request-engagement-with-carrot-cake-ai` | After a quote is agreed, send the details for the contract and deposit invoice. |
| `pay-carrot-cake-ai` | Find out who invoices and where the bank details are. |
| `about-carrot-cake-ai` | Services, pricing, process and business details. |
| `explore-carrot-cake-ai-open-source` | See what Daniel has published, and download Fritter, the English dictation models for technical vocabulary. |

None needs an account or an API key. Skills that send something show the user the content and
ask first. Fritter itself is CC-BY-NC-4.0: free for non-commercial use with attribution.

The skills are in [`plugins/carrot-cake-ai-skills/skills/`](plugins/carrot-cake-ai-skills/skills/),
one folder each.

## Install

**Claude Code:** this repo is a plugin marketplace (`carrot-cake-ai`, plugin
`carrot-cake-ai-skills`).

```
/plugin marketplace add Carrot-Cake-AI/agent-skills
/plugin install carrot-cake-ai-skills@carrot-cake-ai
```

**Any agent:** copy the skill folders into your agent's skills directory, or fetch them from the
site, which lists them at <https://www.carrotcakeai.com/.well-known/agent-skills/index.json>
([Agent Skills Discovery](https://github.com/cloudflare/agent-skills-discovery-rfc) v0.2.0):

```sh
SKILLS_DIR=~/.agents/skills   # your agent's skills folder
SITE=https://www.carrotcakeai.com
curl -s "$SITE/.well-known/agent-skills/index.json" | jq -r '.skills[].name' | while read -r s; do
  mkdir -p "$SKILLS_DIR/$s"
  curl -s -o "$SKILLS_DIR/$s/SKILL.md" "$SITE/.well-known/agent-skills/$s/SKILL.md"
done
```

## How this repo is maintained

The skills are authored on the website and published with sha256 digests in the discovery index
above. **Don't edit the `SKILL.md` files here**, because the sync overwrites them.
`.github/workflows/sync-skills.yml` runs `scripts/sync_skills.py` every day and on demand from the
Actions tab. The script downloads every skill in the index, checks it against its digest, and
writes it under `plugins/carrot-cake-ai-skills/skills/`. It deletes skills the index no longer
lists, and bumps the plugin's patch version when anything changes.

## License

Skills: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), "Carrot Cake AI by Daniel
Rosehill". This covers the skill files only, not the models or projects they point to.
