#!/usr/bin/env python3
"""Pull the official skills from www.carrotcakeai.com into plugins/carrot-cake-ai-skills/skills/.

The website is the source of truth: its SKILL.md files live in the site repo at
website/public/.well-known/agent-skills/<name>/SKILL.md and are published with
an index (Agent Skills Discovery draft v0.2.0) carrying a sha256 per file. This
script downloads every skill in the index, verifies the digest, writes it here,
removes skills no longer listed, and bumps the plugin's patch version when
anything changed. Stdlib only.

Exit 0 always on success; prints "changed" or "unchanged" as the last line.
"""
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path

SITE = "https://www.carrotcakeai.com"
INDEX = f"{SITE}/.well-known/agent-skills/index.json"
ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "carrot-cake-ai-skills" / "skills"
PLUGIN_JSON = ROOT / "plugins" / "carrot-cake-ai-skills" / ".claude-plugin" / "plugin.json"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "carrot-cake-ai-agent-skills-sync"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main() -> int:
    index = json.loads(fetch(INDEX))
    changed = False
    listed = set()
    for skill in index["skills"]:
        name = skill["name"]
        listed.add(name)
        body = fetch(SITE + skill["url"])
        digest = "sha256:" + hashlib.sha256(body).hexdigest()
        if digest != skill["digest"]:
            print(f"{name}: digest mismatch ({digest} != {skill['digest']}); site index is stale, aborting", file=sys.stderr)
            return 1
        dest = SKILLS / name / "SKILL.md"
        if not dest.exists() or dest.read_bytes() != body:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            print(f"updated {name}")
            changed = True
    for d in SKILLS.iterdir() if SKILLS.exists() else []:
        if d.is_dir() and d.name not in listed:
            shutil.rmtree(d)
            print(f"removed {d.name}")
            changed = True
    if changed:
        meta = json.loads(PLUGIN_JSON.read_text())
        major, minor, patch = (int(x) for x in meta["version"].split("."))
        meta["version"] = f"{major}.{minor}.{patch + 1}"
        PLUGIN_JSON.write_text(json.dumps(meta, indent=2) + "\n")
        print(f"plugin version -> {meta['version']}")
    print("changed" if changed else "unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
