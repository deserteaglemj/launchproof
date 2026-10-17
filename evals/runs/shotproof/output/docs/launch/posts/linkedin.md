Status: draft, not posted or submitted. Every step needs the owner's approval.

# LinkedIn (Tue 2026-10-20, about 12:00 PM ET)

Attach `assets/demo.gif` (or `assets/gallery/03-dashboard.jpg`).

---

AI agents are good at turning a screenshot into a web page that looks about right. "About right" is hard to check by eye, so I built a tool that checks it.

shotproof is a free, MIT-licensed plugin for Claude Code and Codex. You give it a screenshot and it writes the HTML + CSS (or React + Tailwind). Then it renders the page in a real browser at the screenshot's size, scores how closely the two match, and fixes the worst-matching part until the score passes. It needs no extra API key, because it uses the model the agent already runs.

I tested it on 8 screens. A fresh agent rebuilt each one from the image alone, and a separate script re-scored each result. All 8 passed, and the fix loop improved the match score by 0.085 SSIM on average.

What it doesn't do yet: identify fonts, or see hover states and animation that a static screenshot can't show.

Code, numbers and per-round logs: https://github.com/deserteaglemj/shotproof
