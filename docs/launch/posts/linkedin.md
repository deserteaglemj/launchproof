# LinkedIn

Status: draft, not posted. Needs owner approval. Voice pass needed: rewrite in your own words (write-like-me) before posting.

Before I made my last plugin public, I scanned its git history. Old commits still had my personal email, my home folder paths and a business name, even though the current files were clean.

So I built launchproof, an open source plugin for Claude Code and Codex. Point it at a finished project and it:
- scans every commit for emails, paths, secrets and private names
- writes the README, community files, CI and a small website
- scores the repo and fixes gaps until it passes
- drafts the launch plan, and leaves every push and post to you

In my evals, two test projects went from 18.5 and 11.1 to 97.2 out of 100. A real repo reached 97.2 but still fails, because a name in its public history needs a rewrite only the owner can approve.

It's MIT licensed: https://github.com/deserteaglemj/launchproof

[image: docs/social-preview.png or assets/scores.png]
