Status: draft, not posted or submitted. Every step needs the owner's approval.

# Reddit drafts

One subreddit per day. Re-read each sidebar and pinned post on the day: self-promotion rules, flair and account-age limits change (all UNVERIFIED here). Reply to every comment. Attach `assets/demo.gif` or a gallery image where images are allowed.

## r/ClaudeAI (Wed 2026-10-21): flair Showcase if offered

**Title:** I built a Claude Code plugin that turns a screenshot into HTML, then scores it against the screenshot and fixes it

I kept getting nice-looking pages from screenshots that didn't actually match, and Claude had no way to tell. So I made shotproof (MIT, no API key; it runs on whatever model your Claude Code session uses).

How it works: Claude writes the page, then a small Python helper renders it in Chromium at the screenshot's exact size. It scores the match with SSIM, overall and in 8 horizontal bands, and Claude fixes the worst band for up to 5 rounds. Console errors, a blank page, a pasted-in screenshot or sideways scroll at 375px fail the check whatever the score.

On my 8-screen eval set all 8 pass, and the fix loop added +0.085 SSIM on average. Every result was re-scored by a separate script; the numbers and per-round logs are in the repo.

Limits: SSIM measures how alike it looks, not code quality. It can't identify fonts. Eight screens is a small set.

Install: `/plugin marketplace add deserteaglemj/shotproof`, then `/plugin install shotproof@shotproof`.

https://github.com/deserteaglemj/shotproof

Happy to hear which screenshots break it.

## r/ClaudeCode (Thu 2026-10-22)

**Title:** shotproof: /shotproof ./design.png → index.html, rendered and SSIM-checked until it passes

Plugin + skill for Claude Code (works in Codex too). The part I care about is the verify loop: `s2c.py verify` renders the page at the screenshot's size and dpr, and writes a side-by-side, a diff heatmap and per-band SSIM. Then the skill makes Claude fix only the worst band (edits, not rewrites) and keep the best round. Max 5 rounds, with fixed pass lines set before the evals ran (0.90, or 0.80 for real sites).

Results: 8/8 eval cases pass, mean +0.085 SSIM from the fix loop, scores re-checked independently. It also has a React + Tailwind mode, though there's only one eval case for it and it's an easy one.

Needs Python 3 + Playwright + Chromium locally. MIT. I built it; feedback welcome.

https://github.com/deserteaglemj/shotproof

## r/SideProject (Fri 2026-10-23)

**Title:** shotproof: screenshot to code that measures whether it actually matches

I built a plugin for Claude Code and Codex. Give it a screenshot and you get one clean HTML file (or React + Tailwind) plus a score for how closely the render matches. It fixes the worst-matching strip of the page until it passes. No API key, MIT, 8 of 8 eval screens pass. The biggest gap is fonts: it picks a system font of the same style.

https://github.com/deserteaglemj/shotproof

## r/coolgithubprojects (Mon 2026-10-26)

**Title:** shotproof: screenshot → HTML/CSS or React + Tailwind in Claude Code/Codex, scored with SSIM and fixed until it passes (MIT)

https://github.com/deserteaglemj/shotproof
