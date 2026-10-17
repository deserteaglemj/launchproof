# shotproof launch plan (v0.4.4)

Status: draft, not posted or submitted. Every step needs the owner's approval.

Prepared 2026-10-17. Channel rules change, so re-read each linked rule page on the day you post. Facts marked UNVERIFIED came from secondary sources.

## Readiness gate

Do not post anywhere until every box is ticked.

- [ ] **History cleaned.** Three old file versions (in commits `2b275c3` to `9f68c65`) contain a private studio name, and those commits are already on `origin/main`. This needs the owner-approved rewrite and force-push in "Owner approval commands", step 1. The current files are clean.
- [ ] Repo is public at https://github.com/deserteaglemj/shotproof (current visibility is not confirmed from this machine).
- [ ] CI green on `main` after the push (`tests` workflow).
- [ ] Release `v0.4.4` published from `docs/releases/v0.4.4.md`.
- [ ] Pages live at https://deserteaglemj.github.io/shotproof/ and the social preview uploaded.
- [ ] Quickstart tried on a clean machine: `/plugin marketplace add deserteaglemj/shotproof`, `/plugin install shotproof@shotproof`, the helper setup line, then `/shotproof ./some.png`.
- [ ] The owner can answer comments for 4 to 6 hours after Show HN and Product Hunt.

Current state (2026-10-17): `lp.py audit . --rev main` scores **97.2/100**. The only failure is `hygiene-history` (the item above). Self-tests pass 11 of 11. `claude plugin validate --strict` passes for the plugin and the marketplace.

## Facts every post may use

Copy only these. All come from the README proof section and [`evals/RESULTS.md`](../../evals/RESULTS.md).

- Plugin for Claude Code and Codex. Turns a screenshot into HTML + CSS (one file, no CDN or web fonts) or React + Tailwind, using the agent's own model. No API key.
- Renders in Chromium at the screenshot's size and dpr, scores with grayscale SSIM overall and in 8 horizontal bands, and fixes the worst band for up to 5 rounds against a fixed pass line.
- Console errors, failed requests, a blank page, a pasted screenshot or sideways scroll at 375px fail the check whatever the score.
- 8 of 8 eval cases pass: six pages written for the test (one React + Tailwind) at 0.90, two real public sites at 0.80. Both pass lines were set before the runs. Each case was rebuilt by a fresh agent that saw only the screenshot and the skill, then re-scored by a separate script.
- The fix loop added +0.085 SSIM on average (round 1 mean 0.862, final mean 0.946). Final scores range from 0.865 to 0.9996.
- Limitations: SSIM measures visual match, not code quality. Static frame only. No font identification. Small eval set. The one React case is easy (its source used Tailwind defaults). Needs local Python, Playwright and Chromium.
- MIT. Built by Marquis Jackson (disclose this in every post).

## Sequence

All times are US Eastern (ET) unless marked PT.

| Day | Date | Channel | Time | Owner action | Needs |
| --- | --- | --- | --- | --- | --- |
| 0 | Mon 2026-10-19 | GitHub | Morning | Run the owner approval commands, steps 1 to 7 | Approval for the history rewrite and force-push |
| 0 | Mon 2026-10-19 | Claude plugin directory | After Pages is live | Submit from https://claude.ai/directory/manage ([posts/directories.md](posts/directories.md)) | Public repo, validate passes |
| 1 | Tue 2026-10-20 | Show HN | 8:30 AM ET | Write the post by hand from [posts/show-hn.md](posts/show-hn.md), post, add the first comment | Established HN account; free until about 2 PM |
| 1 | Tue 2026-10-20 | X, LinkedIn, Bluesky / Mastodon | 12:00 PM ET | Post [posts/x.md](posts/x.md), [posts/linkedin.md](posts/linkedin.md), [posts/bluesky-mastodon.md](posts/bluesky-mastodon.md) | `assets/demo.mp4` or `assets/demo.gif` |
| 2 | Wed 2026-10-21 | r/ClaudeAI | 10:00 AM ET | Post from [posts/reddit.md](posts/reddit.md) | Re-read the sub rules; Showcase flair (UNVERIFIED) |
| 3 | Thu 2026-10-22 | r/ClaudeCode | 10:00 AM ET | Post the r/ClaudeCode version | Re-read the sub rules |
| 3 | Thu 2026-10-22 | Dev.to | 11:00 AM ET | Publish [posts/devto.md](posts/devto.md) | Dev.to account; canonical URL set to the repo |
| 4 | Fri 2026-10-23 | r/SideProject | 10:00 AM ET | Post the r/SideProject version | Re-read the sub rules |
| 5 | Sat 2026-10-24 | Discord / Slack | Any | Share in #showcase-type channels only ([posts/discord-slack.md](posts/discord-slack.md)) | Membership in each community |
| 6 | Mon 2026-10-26 | r/coolgithubprojects | 10:00 AM ET | Post the short version | Re-read the sub rules |
| 8 | Tue 2026-10-27 | Product Hunt | 12:01 AM PT | Launch from [posts/product-hunt.md](posts/product-hunt.md) | 4+ gallery images, maker comment, a full day present |
| 14 | Sat 2026-10-31 | awesome-claude-code | Any | Submit the web issue form ([posts/directories.md](posts/directories.md)) | First eligible date (14 days old) |
| 14+ | 2026-10-31 onward | Other awesome lists, Codex list, newsletters | Any | [posts/directories.md](posts/directories.md), [posts/newsletters.md](posts/newsletters.md) | Each list's eligibility rules |

## Channels

### Show HN
https://news.ycombinator.com/showhn.html. People can try it now with no signup. HN asks that the text be written by hand, so [posts/show-hn.md](posts/show-hn.md) is an outline and facts only. Title format: `Show HN: shotproof – ...`, no superlatives. Do not ask anyone to upvote.

### Reddit
r/ClaudeAI, r/ClaudeCode, r/SideProject and r/coolgithubprojects, one per day with different wording. Skipped: r/programming (usually no self-promotion) and r/opensource (strict, and the tool is agent-specific). r/codex or r/OpenAI only if their rules allow tool posts on the day (UNVERIFIED). Reply to every comment.

### X, Bluesky, Mastodon
A five-post thread with the demo video. Tag @AnthropicAI or @OpenAI only if you want to; the tool does run on their agents.

### LinkedIn
One first-person post with the demo GIF.

### Product Hunt
Day 8 at 12:01 AM PT (UNVERIFIED as best practice). Gallery: `assets/gallery/*.jpg`, `docs/social-preview.png`, `assets/demo.mp4`.

### Dev.to
One technical article: how the render, score and fix loop works, and the numbers. Hashnode skipped: same audience, so one article is enough.

### Discord and Slack
Only in channels made for sharing (Claude Developers Discord or similar, if it has a showcase channel). Read the pinned rules first.

### Plugin and skill directories
Claude plugin directory on day 0 (review takes time). Codex: no confirmed official directory; the repo marketplace is the install route. Skill registries and awesome lists follow their own eligibility dates. See [posts/directories.md](posts/directories.md) and [LISTINGS.md](LISTINGS.md).

### Newsletters
Changelog News and Console.dev after day 7. See [posts/newsletters.md](posts/newsletters.md).

## Owner approval commands

Run in order, from the repo folder, only after approving each one. Nothing below has been run.

1. **History rewrite** (removes the private studio name from three old file versions; `origin/main` already holds those commits):

   ```bash
   git bundle create ../shotproof-before-rewrite.bundle --all
   # replacements.txt lives OUTSIDE the repo, one line per name in the private names file, e.g.:
   #   <private studio name>==>the studio
   python3 -m pip install git-filter-repo
   git filter-repo --replace-text ../shotproof-replacements.txt --force
   git remote add origin https://github.com/deserteaglemj/shotproof.git   # filter-repo removes the remote
   python3 <path-to>/lp.py hygiene . --rev main --names ../shotproof-names.txt   # must show 0 blocking
   ```

   Tags `v0.3.0` to `v0.4.3` are rewritten too. If the repo was ever public, forks and caches may still hold the old commits. Contact GitHub Support to purge cached views if that matters.

2. Commit this work (the local repo is already set to the noreply email), tag, and push:

   ```bash
   git add -A && git commit -m "shotproof 0.4.4: community files, launch prep"
   git tag v0.4.4
   git push --force-with-lease origin main
   git push --force origin --tags
   ```

   Without the rewrite, use `git push origin main --follow-tags` instead.

3. Visibility, if not yet public: `gh repo edit deserteaglemj/shotproof --visibility public --accept-visibility-change-consequences`
4. Metadata: the `apply_with` command in [repo-metadata.json](repo-metadata.json).
5. Pages: `gh api -X POST repos/deserteaglemj/shotproof/pages -f "source[branch]=main" -f "source[path]=/docs"` (skip if Pages is already on).
6. Release: `gh release create v0.4.4 --title "shotproof v0.4.4" --notes-file docs/releases/v0.4.4.md`
7. Social preview: upload `docs/social-preview.png` in Settings > General > Social preview (there is no API for this).
8. Then each post and submission in the sequence table, one at a time.
