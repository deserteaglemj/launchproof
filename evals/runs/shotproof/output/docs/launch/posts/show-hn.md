Status: draft, not posted or submitted. Every step needs the owner's approval.

# Show HN: outline only (write the final text by hand)

HN moderators ask that Show HN text be written by the author, not generated. Use this as notes and write the post and first comment in your own words.

- **When:** Tue 2026-10-20, about 8:30 AM ET. Be free to answer until about 2 PM.
- **Needs:** an established HN account. Link: https://github.com/deserteaglemj/shotproof

## Title options (pick one, edit freely)

- Show HN: shotproof – screenshot to HTML in Claude Code, scored against the screenshot
- Show HN: shotproof – a Claude Code/Codex plugin that checks its screenshot-to-code output

## First comment: points to cover

1. **Why:** agents write plausible-looking UI from a screenshot, and nobody checks it against the image. I wanted the agent to measure the result itself.
2. **How:** the agent writes the page, then `s2c.py verify` renders it in Chromium at the screenshot's size and dpr. It scores grayscale SSIM overall and in 8 bands, and the agent fixes the worst band with targeted edits for up to 5 rounds. Console errors, failed requests, a blank page, a pasted screenshot or sideways scroll at 375px fail regardless of score.
3. **No key:** it uses the model your Claude Code or Codex session already runs. The render and scoring run locally.
4. **Numbers:** 8 of 8 eval cases pass (0.90 pass line for own pages, 0.80 for two real sites, both set before the runs). The fix loop added +0.085 SSIM on average. Every page was re-scored by a separate script. All in `evals/RESULTS.md`.
5. **Weak spots:** SSIM is not code quality. No font identification (the serif case hit the 5-round cap). The React case is easy because its source used Tailwind defaults. Only 8 screens.
6. **Prior art:** abi/screenshot-to-code is a full web app with more stacks and video input. This one is for people who already work inside an agent.
7. **Ask:** which screenshots break it? Is SSIM the wrong metric for this?

Say plainly that you built it. Do not ask for upvotes.
