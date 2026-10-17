# Show HN (outline only)

Status: draft, not posted. Needs owner approval. Voice pass needed: rewrite in your own words (write-like-me) before posting.

HN asks that Show HN text be written by hand, not by an LLM. Use this outline and the facts; write the post yourself.

**Title (under 80 characters):** Show HN: Launchproof - make a finished project safe and ready to publish on GitHub

**URL:** https://github.com/deserteaglemj/launchproof

**First comment, points to cover in your words:**
- Why: you built a plugin, went to make it public, and a scan of its history turned up a personal email, home paths and a business name in old commits. The fix was manual and easy to miss.
- What it does: a Claude Code and Codex skill that scans every commit for emails, home paths, secrets and private names, writes the README and community files, scores the repo on a 0 to 100 checklist, loops until 90+, and drafts a launch plan. It never pushes or posts.
- How it is checked: 3 eval cases run headless with push and history rewrites denied. Two seeded fixtures went from 18.5 and 11.1 to 97.2. A real repo went from 77.8 to 97.2 and still fails, because a business name sits in its public history. The first eval round failed outright (a skill-loading bug); both rounds are in the repo.
- Limits: the checklist measures structure and evidence, not writing quality; 10 secret patterns (runs gitleaks if installed).
- Ask: what checks would you add before you make a repo public?
