Status: draft, not posted or submitted. Every step needs the owner's approval.

# Bluesky / Mastodon (Tue 2026-10-20, about 12:00 PM ET)

Each post fits in 300 characters (Bluesky's limit). Attach `assets/demo.gif` with alt text: "Screenshot in, code out, scored and fixed until it passes."

1. I built shotproof, a Claude Code + Codex plugin: screenshot in, HTML + CSS (or React + Tailwind) out. Then it renders the page, scores it against the screenshot with SSIM and fixes the worst band until it passes. No API key, MIT.

2. On 8 eval screens all 8 pass, with +0.085 mean SSIM from the fix loop, re-scored by a separate script. Limits: no font identification, and SSIM is not code quality. https://github.com/deserteaglemj/shotproof

Mastodon hashtags: #ClaudeCode #WebDev #OpenSource
