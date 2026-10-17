Status: draft, not posted or submitted. Every step needs the owner's approval.

# X thread (Tue 2026-10-20, about 12:00 PM ET, after Show HN)

Attach `assets/demo.mp4` to post 1. Link to the repo, not the HN thread.

1/ I built shotproof: a Claude Code and Codex plugin that turns a screenshot into HTML + CSS (or React + Tailwind), then checks its own work against the screenshot. No API key. MIT.

2/ The check is the point. It renders the page in Chromium at the screenshot's exact size and scores it with SSIM, overall and in 8 bands. Then the agent fixes the worst band, up to 5 rounds.

3/ Console errors, a blank page, a pasted-in screenshot or sideways scroll at 375px fail the check, however good the score looks.

4/ Evals: 8 of 8 screens pass (pass lines set before the runs). The fix loop added +0.085 SSIM on average, and every page was re-scored by a separate script. Logs are in the repo.

5/ Limits: SSIM measures visual match, not code quality. No font identification. Small eval set.
https://github.com/deserteaglemj/shotproof
