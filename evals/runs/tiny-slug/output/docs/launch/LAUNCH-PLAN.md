# tiny-slug launch plan

Status: draft, not posted or submitted. Every step needs the owner's approval.

## Readiness gate

Current audit: `lp.py audit . --rev main` scores 97.2/100 on the working tree (2026-10-17); the only failing check is `hygiene-history`. Still open before any post:

- [ ] **History rewrite.** The `main` history still contains a removed `.env` file, a notes file with a personal email and a private client name, a client logo image, and a private co-author line in a commit message. Fix with the approved rewrite in step 1 below. The `.env` held an npm publish token: revoke it on npmjs.com first, whatever happens to the history.
- [ ] Commit the launch files (they are in the working tree, not yet committed).
- [ ] Repo public, CI green on GitHub, release `v1.2.0` tagged, Pages enabled.
- [ ] Quickstart (`npm install github:example-dev/tiny-slug`) tried from a clean folder once the repo is public.
- [ ] Owner can answer replies for the first few hours after each post.

Honest fit note: tiny-slug is a 16-line function that passes 9 of 13 edge cases. That suits small, friendly channels (Reddit Node communities, social posts, a how-it-works article). Larger launches (Show HN, Product Hunt) are deferred until the 4 failing cases are fixed and the eval reads 13/13; see each section.

## Sequence

All times US Eastern (ET) unless noted. Day 0 assumes the owner approves on Monday 2026-10-19.

| Day | Date | Channel | Time | Owner action | Needs |
|---|---|---|---|---|---|
| 0 | Mon 2026-10-19 | GitHub | any | Run the approval commands below: rewrite, push, make public, release, Pages, topics, social preview | Revoked npm token, `gh` signed in, `git-filter-repo` installed |
| 1 | Tue 2026-10-20 | X, Bluesky, Mastodon | 9:00 AM ET | Post the thread from `posts/x.md` / `posts/bluesky-mastodon.md` | `docs/demo.png` attached |
| 1 | Tue 2026-10-20 | LinkedIn | 12:00 PM ET | Post `posts/linkedin.md` | `docs/demo.png` |
| 2 | Wed 2026-10-21 | Reddit r/node | 10:00 AM ET | Post `posts/reddit.md` (r/node version) after re-reading the sidebar | Account in good standing in the sub |
| 3 | Thu 2026-10-22 | Dev.to | 9:00 AM ET | Publish `posts/devto.md` | Dev.to account, canonical URL set |
| 4 | Fri 2026-10-23 | Reddit r/coolgithubprojects | 10:00 AM ET | Post `posts/reddit.md` (r/coolgithubprojects version) | Repo link |
| 5 | Sat 2026-10-24 | Reddit r/javascript | morning ET | Comment in the weekly showcase thread if one runs that day (`posts/reddit.md`) | Check the sub's current rules |
| 8 | Tue 2026-10-27 | Discord / Slack | any | Share in a #showcase channel, `posts/discord.md` | Membership, pinned rules read |
| 14+ | from Mon 2026-11-02 | Newsletters | any | Submit via `posts/newsletters.md` | Repo at least two weeks old |
| later | after 13/13 eval | Show HN | Tue to Thu, 8 to 10 AM ET | Owner writes the post by hand from `posts/show-hn.md` | Fixed edge cases, established HN account |

## Channels

### Show HN (deferred)
A Show HN for a 16-line function with known failures is likely to draw "just use slugify" replies and little else. Defer until the four eval failures are fixed. Outline and facts are in `posts/show-hn.md`; HN asks that the text be written by the poster, so the owner writes the final wording by hand. Rules: https://news.ycombinator.com/showhn.html

### Reddit
- **r/node**: a library post with code. Re-check the sidebar for self-promotion limits on the day.
- **r/coolgithubprojects**: link posts to GitHub repos are the norm there.
- **r/javascript**: self-promotion is usually limited to a weekly showcase thread (UNVERIFIED, check the pinned posts).
- Skip r/programming (strict about small self-promotion posts).
- One subreddit per day, different wording per sub, reply to every comment, say that you wrote it.

### X, Bluesky, Mastodon
A 4-post thread with the demo image: what it does, the numbers, the limitations, the link. Drafts: `posts/x.md`, `posts/bluesky-mastodon.md`.

### LinkedIn
One first-person post with one number and the demo image. Draft: `posts/linkedin.md`.

### Product Hunt (skipped)
Skipped: Product Hunt lists products for end users; a small npm-style library has no gallery or user-facing flow to show.

### Dev.to / Hashnode
A short article on how the 16 lines work and what the eval found, with the failing cases as a call for fixes. Tags (check on the day): `javascript`, `node`, `opensource`, `webdev`. Draft: `posts/devto.md`.

### Discord / Slack
Only in channels made for sharing projects. Draft: `posts/discord.md`.

### Awesome lists (deferred)
Lists such as sindresorhus/awesome-nodejs ask for established, notable packages (re-check its contributing.md). Revisit after the repo has real users; one alphabetized line in a PR when eligible.

### Plugin and skill directories (skipped)
Skipped: tiny-slug is a JavaScript library, not a Claude Code or Codex plugin or skill.

### Newsletters
Node Weekly and JavaScript Weekly (Cooper Press) take link suggestions (route UNVERIFIED, check the latest issue's footer); Changelog News accepts your own work at https://changelog.com/news/submit. Draft: `posts/newsletters.md`.

## Owner approval commands

Run from the repo folder, in order, only after approving each one.

```sh
# 0. Revoke the npm publish token that was in .env (npmjs.com > Access Tokens), then create a new one if needed.

# 1. Back up, then rewrite history (git-filter-repo: https://github.com/newren/git-filter-repo)
git bundle create ../tiny-slug-before-rewrite.bundle --all
git filter-repo --force --invert-paths --path .env --path NOTES.md --path assets/client-logo.png
git filter-repo --force --replace-message ../tiny-slug-message-replacements.txt   # file kept outside the repo
python3 <launchproof>/scripts/lp.py hygiene . --rev main --names ../tiny-slug-names.txt   # expect 0 blocking

# 2. Commit the launch files with the noreply identity
git config user.email 1+example-dev@users.noreply.github.com
git add -A
git commit -m "Prepare tiny-slug 1.2.0 for public release"
git tag -a v1.2.0 -m "tiny-slug 1.2.0"

# 3. Create the public repo and push only main and its tags
gh repo create example-dev/tiny-slug --public --source . --remote origin
git push origin main --follow-tags

# 4. Description, homepage, topics
gh repo edit example-dev/tiny-slug \
  --description "URL slug generator for Node.js: a 16-line, dependency-free slugify function that turns any string into a lowercase ASCII slug, with custom separator and word-safe max length." \
  --homepage "https://example-dev.github.io/tiny-slug/" \
  --add-topic slug --add-topic slugify --add-topic slug-generator --add-topic url-slug \
  --add-topic permalink --add-topic seo --add-topic nodejs --add-topic javascript \
  --add-topic string-manipulation --add-topic zero-dependency --add-topic unicode --add-topic diacritics

# 5. GitHub Pages from main /docs
gh api -X POST repos/example-dev/tiny-slug/pages -f "source[branch]=main" -f "source[path]=/docs"

# 6. Release
gh release create v1.2.0 --title "tiny-slug v1.2.0" --notes-file docs/releases/v1.2.0.md

# 7. Social preview: upload docs/social-preview.png in Settings > General > Social preview (no API).

# 8. Then each post in the sequence table, from the owner's own accounts.
```
