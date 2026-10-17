Status: draft, not posted or submitted. Every step needs the owner's approval.

# Dev.to article (Thu 2026-10-22, about 11:00 AM ET)

- **Tags (4 max, check what's popular on the day):** ai, webdev, opensource, python
- **Canonical URL:** https://github.com/deserteaglemj/shotproof
- **Cover image:** `docs/social-preview.png`

---

# Making an AI agent prove its screenshot-to-code output matches

Ask a coding agent to turn a screenshot into HTML and you'll get something close. How close is hard to judge by eye, and the agent can't see its own result at all. I built shotproof to close that loop: it's a plugin for Claude Code and Codex that renders what the agent wrote, measures it against the screenshot and makes the agent fix what's off.

## The loop

1. **Read.** The agent maps sections with pixel ranges, copies text exactly, and samples colors from real pixels (`s2c.py palette`).
2. **Build.** By default it writes one `index.html` with inline CSS and no CDN or web fonts, so it renders the same everywhere. React + Tailwind is optional.
3. **Render and compare.** `s2c.py verify` opens the page in headless Chromium at the screenshot's size and device scale. It writes a side-by-side image, a diff heatmap, a grayscale SSIM score and a score for each of 8 horizontal bands. It also reports how far each band's content is shifted vertically.
4. **Fix the worst band.** After round 1 the agent may only make targeted edits. It keeps the best-scoring round and stops at the pass line or after 5 rounds.
5. **Hard fails.** Console errors, failed requests, a blank page, one image covering more than a quarter of the page (pasting the screenshot in) or sideways scroll at 375px fail the check, whatever the score.

## Does it work?

I set up 8 cases. Six are pages I wrote, so the right answer is known, and one of those is a React + Tailwind app. The other two are real public sites captured read-only. Pass lines were fixed before running: 0.90 SSIM for my pages and 0.80 for the real sites. A fresh agent rebuilt each case from the screenshot alone, and a separate script re-scored every final page.

All 8 passed. The fix loop raised SSIM by 0.085 on average (round 1 mean 0.862, final mean 0.946). Final scores ran from 0.865 (Hacker News) to 0.9996 (the React case). Full table and per-round logs: [evals/RESULTS.md](https://github.com/deserteaglemj/shotproof/blob/main/evals/RESULTS.md).

## What it doesn't do

- SSIM measures how alike two images look. It says nothing about code quality or accessibility.
- No font identification. It picks a system font of the same style, which is why the serif article case needed all 5 rounds.
- The React case scored so high partly because its source used Tailwind's defaults. React mode is untested on designs built outside them.
- Eight screens is a small set.

## Try it

```text
/plugin marketplace add deserteaglemj/shotproof
/plugin install shotproof@shotproof
/shotproof ./screenshot.png
```

One-time setup: `python3 -m pip install playwright pillow numpy && python3 -m playwright install chromium`. In Codex, use `codex plugin marketplace add deserteaglemj/shotproof`. MIT licensed. I built it, and I'd like to hear where it breaks.
