Status: draft, not posted or submitted. Every step needs the owner's approval.

# Newsletter tips (from Mon 2026-10-26)

- **Changelog News:** https://www.changelog.com/news/submit (sign-in required; accepts your own work).
- **Console.dev:** https://console.dev/selection-criteria (editorial tips by email; developer-first tools only).
- **Claude Code or AI-tools weeklies:** find the submission link in the latest issue.
- Skipped: TLDR and Hacker Newsletter. No verified submission route.

## Pitch (keep it short)

**Subject:** shotproof: screenshot to code that checks it matches (Claude Code and Codex plugin, MIT)

shotproof is a plugin for Claude Code and Codex. It turns a screenshot into HTML + CSS or React + Tailwind using the agent's own model (no API key). Then it renders the page in Chromium, scores it against the screenshot with SSIM in 8 bands, and fixes the worst band until a fixed pass line is met. 8 of 8 eval screens pass, with +0.085 SSIM on average from the fix loop, re-scored independently. Limits: no font identification, and the eval set is small. I built it.

https://github.com/deserteaglemj/shotproof
