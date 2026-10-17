Status: draft, not posted or submitted. Every step needs the owner's approval.

# Plugin directories, skill registries and awesome lists

The full paste-ready fields per target are in [../LISTINGS.md](../LISTINGS.md). This file gives the order and dates.

| When | Target | Route | Eligibility |
| --- | --- | --- | --- |
| Mon 2026-10-19 (day 0) | Claude plugin directory | https://claude.ai/directory/manage. Pre-check: https://www.claude.com/docs/plugins/pre-submission-checklist | Public repo. `claude plugin validate --strict` passes for the plugin and the marketplace (checked 2026-10-17) |
| Sat 2026-10-31 | hesreallyhim/awesome-claude-code | Web issue form only (no PRs, no CLI-made issues) | 14 days old or 100+ stars. One-line plain description, no emoji |
| 2026-10-31 onward | hashgraph-online/awesome-codex-plugins | PR adding one alphabetized line | Their `plugin-scanner` must score 80/130+ with no critical or high findings. Not run yet |
| When eligible | VoltAgent/awesome-agent-skills, travisvn/awesome-claude-skills, ComposioHQ/awesome-claude-skills | PR | Each needs real outside usage or social proof first |
| Check first | skills.sh, claude-plugins.dev | Registry (submission route UNVERIFIED) | Test `npx skills add deserteaglemj/shotproof` on a clean machine before promoting it |
| n/a | Official Codex directory | None confirmed | Install route stays `codex plugin marketplace add deserteaglemj/shotproof` |

## Short description (all directories)

Claude Code and Codex plugin that turns a screenshot into HTML/CSS or React + Tailwind with no API key, then renders, scores (SSIM) and fixes it until it matches.
