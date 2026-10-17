Status: draft, not posted or submitted. Every step needs the owner's approval.

# Product Hunt (Tue 2026-10-27, 12:01 AM PT)

Needs: a maker account, the whole day free to reply, and the gallery below. https://www.producthunt.com/launch

- **Name:** shotproof
- **Tagline (under 60 characters):** Screenshot to code that checks it matches (49 characters)
- **Topics:** Developer Tools, Artificial Intelligence, Open Source, Design Tools
- **Link:** https://github.com/deserteaglemj/shotproof
- **Gallery:** `docs/social-preview.png`, `assets/gallery/04-mobile-login.jpg`, `assets/gallery/03-dashboard.jpg`, `assets/gallery/01-saas-landing.jpg`, `assets/gallery/08-react-settings.jpg`, video `assets/demo.mp4`
- **Pricing:** Free (MIT)

## Description (under 260 characters)

A Claude Code and Codex plugin: screenshot in, HTML + CSS or React + Tailwind out. It renders the result, scores it against your screenshot with SSIM and fixes it until it passes. No API key.

## Maker comment

Hi PH, I'm Marquis and I built shotproof.

Agents can turn a screenshot into a page, but nothing tells them whether it matches. shotproof adds that check. It renders the page in Chromium at the screenshot's size, scores the match overall and in 8 horizontal bands, and has the agent fix the worst band for up to 5 rounds. A blank page, console errors, a pasted-in screenshot or sideways scroll on a phone width fail the check whatever the score.

I tested it on 8 screens and all 8 passed. The fix loop improved the score by 0.085 SSIM on average, and a separate script re-scored every result (all in the repo).

It can't identify fonts yet and can't see hover states. I'd love to hear which screenshots trip it up.
