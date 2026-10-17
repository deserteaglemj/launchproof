# wordfreq launch plan

Status: draft, not posted or submitted. Every step needs the owner's approval.

## Readiness gate

- Audit: `python3 lp.py audit . --rev main` scored **97.2/100** on 2026-10-17. The only required failure left is `hygiene-history`.
- Open before any public step:
  1. **History rewrite (blocking).** Commit `2ab3ab6` has a personal author/committer email, a home path in `scripts/bench.sh`, and an AWS access key in `settings.py` (deleted in `f17947c` but still in history). Rotate the key first, then rewrite (commands in "Owner approval commands").
  2. **Name collision (decide).** `wordfreq` is already a well-known PyPI package (rspeer/wordfreq). Readers will confuse the two. The README and FAQ say so, but consider renaming (for example `wfcount`) before launch. If you rename, update every file that says `wordfreq` and rerun the audit.
  3. CI must be green on GitHub after the first push (only run locally so far).
  4. Quickstart `pip install git+https://github.com/example-dev/wordfreq` only works once the repo is public; test it from a clean machine.
- Expectation check: this is a ~30-line CLI. Treat Show HN and Reddit as feedback channels, not traffic goals. Product Hunt is skipped.

## Sequence

| Day | Date | Channel | Time (with zone) | Owner action | Needs |
|---|---|---|---|---|---|
| 0 | Mon 2026-10-19 | GitHub | any | Rewrite history, push, make public, release v0.3.0, enable Pages, set topics and social preview | Rotated key, approval of each command |
| 1 | Tue 2026-10-20 | Show HN | 09:00 ET | Write post by hand from `posts/show-hn.md`, post, stay for 4 to 6 hours | Established HN account |
| 1 | Tue 2026-10-20 | X, Bluesky/Mastodon, LinkedIn | 14:00 ET | Post `posts/x.md`, `posts/bluesky-mastodon.md`, `posts/linkedin.md` | `docs/demo.svg` exported as PNG |
| 2 | Wed 2026-10-21 | r/commandline | 10:00 ET | Post from `posts/reddit.md` | Re-read sub rules that day |
| 3 | Thu 2026-10-22 | r/Python | 10:00 ET | Post from `posts/reddit.md` (Showcase rules) | Re-read sub rules that day |
| 4 | Fri 2026-10-23 | r/coolgithubprojects | 10:00 ET | Post from `posts/reddit.md` | |
| 5 | Mon 2026-10-26 | Dev.to | 09:00 ET | Publish `posts/devto.md` | Dev.to account |
| 6 | Tue 2026-10-27 | Discord/Slack | 12:00 ET | Share in a showcase channel (`posts/discord.md`) | Membership, pinned rules |
| 14+ | from Mon 2026-11-02 | Newsletters, awesome lists | any | Submit per `posts/newsletters.md`, `posts/awesome-lists.md` | Repo age/stars thresholds |

## Channels

### Show HN
Fits: free, try-it-now, own work. Title idea: `Show HN: wordfreq - count the most common words across text files`. HN asks for hand-written text, so `posts/show-hn.md` is an outline only. Never ask for upvotes.

### Reddit
r/commandline, r/Python (self-promotion goes in Showcase posts with required sections; UNVERIFIED, re-check), r/coolgithubprojects. One sub per day, different wording, reply to every comment. Skip r/programming (usually no self-promotion) and r/opensource (strict, low fit for a tiny CLI).

### X, Bluesky, Mastodon
Short thread with the demo image, the one-line command, the eval result, the accented-word limitation, the link.

### LinkedIn
One first-person post. Low expected fit for a hobby CLI; optional.

### Product Hunt
Skipped: a 30-line CLI with no gallery-worthy UI is a poor fit for a full launch day.

### Dev.to / Hashnode
One article: how word counting goes wrong (case, apostrophes, encodings), the eval cases, the limitation. Tags: `python`, `cli`, `opensource`, `beginners` (check on the day).

### Discord / Slack
Python community servers with a showcase channel only. Read pinned rules first.

### Awesome lists
Day 14+. Candidates in `posts/awesome-lists.md`; most require traction. Do not submit until a list's CONTRIBUTING criteria are met.

### Plugin and skill directories
Skipped: wordfreq is not a Claude Code or Codex plugin or skill.

### Newsletters
Changelog News (own work accepted), PyCoder's Weekly (submission link UNVERIFIED). See `posts/newsletters.md`.

## Owner approval commands

Run in this order, from the repo root, only after approving each one.

```sh
# 1. Rotate the AWS access key that was in settings.py (AWS console: IAM > Users > Security credentials). Do this first.

# 2. Commit the launch prep, back up, then rewrite history (needs git-filter-repo;
#    --force because this is not a fresh clone, and the bundle is the backup)
git add -A && git commit -m "Prepare v0.3.0 for public release"
git bundle create ../wordfreq-before-rewrite.bundle --all
printf 'Dev Person <1+example-dev@users.noreply.github.com> <%s>\n' "$(git log -1 --format=%ae 2ab3ab6)" > ../mailmap.txt
printf 'regex:/Users/[^/ ]+/corpus==>corpus\n' > ../replacements.txt
git filter-repo --mailmap ../mailmap.txt --replace-text ../replacements.txt --invert-paths --path settings.py --force
python3 lp.py hygiene . --rev main   # expect 0 blocking

# 3. Tag, create the public repo and push main with tags
git tag v0.3.0
gh repo create example-dev/wordfreq --public --source . --remote origin
git push origin main --follow-tags

# 4. Metadata (from docs/launch/repo-metadata.json)
gh repo edit example-dev/wordfreq --description "Word frequency counter CLI for plain text files: prints the most common words, with stop-word filtering, using only the Python standard library." --homepage "https://example-dev.github.io/wordfreq/" --add-topic word-frequency --add-topic word-count --add-topic word-counter --add-topic text-analysis --add-topic text-processing --add-topic cli --add-topic command-line-tool --add-topic python --add-topic python3 --add-topic stop-words --add-topic corpus-linguistics --add-topic no-dependencies

# 5. Pages from main /docs
gh api -X POST repos/example-dev/wordfreq/pages -f "source[branch]=main" -f "source[path]=/docs"

# 6. Release
gh release create v0.3.0 --title "wordfreq v0.3.0" --notes-file docs/releases/v0.3.0.md

# 7. Social preview: upload docs/social-preview.png in Settings > General > Social preview (no API).
# 8. Posts and submissions in the order of the Sequence table above.
```
