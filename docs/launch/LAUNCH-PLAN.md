# launchproof launch plan

Status: draft, not posted or submitted. Every step needs Quis's approval and is sent from his own accounts.

## Readiness gate

| Check | State on 2026-10-17 |
|---|---|
| Repo public, CI green, release v0.1.0 tagged | see the final report of the build session |
| `lp.py audit . --rev main` | scored in CI on every push (must be 90+) |
| Hygiene scan of main | clean (CI step) |
| Quickstart tested from a clean install | Claude Code and Codex install proven locally (see report) |
| Owner free to answer comments for 4 to 6 hours after each big post | Quis to confirm per day |

Facts to use everywhere (from [evals/RESULTS.md](../../evals/RESULTS.md)): 3 eval cases, 2 pass; scores 18.5 to 97.2 and 11.1 to 97.2 on seeded fixtures (100.0 after the owner-approved rewrite), 77.8 to 97.2 on a real repo that still fails on a private name in its history; the agent never pushed, added a remote or rewrote history. Limitation to mention: the audit checks structure and evidence, not writing quality.

## Sequence

| Day | Date (suggested) | Time | Channel | Owner action | Needs |
|---|---|---|---|---|---|
| 0 | Mon 2026-10-19 | any | GitHub | Confirm topics, Pages, social preview upload | Settings access |
| 0 | Mon 2026-10-19 | any | Claude plugin directory | Submit at claude.ai/directory/manage, run Validate | Public repo |
| 1 | Tue 2026-10-20 | 8 to 10 AM ET | Show HN | Rewrite [posts/show-hn.md](posts/show-hn.md) in your own words, post, stay 4 to 6 hours | Established HN account |
| 1 | Tue 2026-10-20 | after HN, 12 PM ET | X, Bluesky, Mastodon | Post [posts/x.md](posts/x.md) thread with the score chart | `assets/scores.png` |
| 1 | Tue 2026-10-20 | 12 PM ET | LinkedIn | Post [posts/linkedin.md](posts/linkedin.md) | Social preview image |
| 2 | Wed 2026-10-21 | 9 AM ET | Reddit r/ClaudeAI | Post [posts/reddit.md](posts/reddit.md) (ClaudeAI version), Showcase flair if offered | Account older than a few days |
| 3 | Thu 2026-10-22 | 9 AM ET | Reddit r/ClaudeCode | Post the ClaudeCode version | Read sidebar first |
| 4 | Fri 2026-10-23 | 9 AM ET | Dev.to (or Hashnode) | Publish [posts/devto.md](posts/devto.md) | Dev.to account |
| 5 | Sat 2026-10-24 | any | Reddit r/SideProject weekly thread, r/coolgithubprojects | Short versions in [posts/reddit.md](posts/reddit.md) | Read rules |
| 6 to 7 | Oct 25 to 26 | any | Discord and Slack | [posts/discord-slack.md](posts/discord-slack.md) in showcase channels only | Membership |
| 8+ | from Tue 2026-10-27 | 12:01 AM PT | Product Hunt (optional) | [posts/product-hunt.md](posts/product-hunt.md) | Gallery, maker comment, a free day |
| 14+ | from Mon 2026-11-02 | any | awesome-claude-code | Issue form only, once the repo is 14+ days old and has 100+ stars | Eligibility |
| 14+ | from Mon 2026-11-02 | any | Newsletters | [posts/newsletters.md](posts/newsletters.md) | Some traction to point to |
| ongoing | | | Codex, skill registries | [posts/directories.md](posts/directories.md) | Check each route |

## Channels

### Show HN
Fits: it is something people can install and try today, with no signup. HN asks for hand-written text, so the draft is an outline and facts only. Never ask anyone to upvote.

### Reddit
r/ClaudeAI and r/ClaudeCode are the closest audiences; r/SideProject and r/coolgithubprojects allow project posts. Self-promotion rules vary and change: read each sidebar on the day (UNVERIFIED specifics). One subreddit per day, different wording each, reply to every comment. Skip r/programming (strict self-promotion rules) unless a mod approves.

### X, Bluesky, Mastodon
One thread with the score chart and an honest limitation. Tag nobody unless the post is truly about their product.

### LinkedIn
One first-person post about why publishing safely matters (history leaks), with the chart.

### Product Hunt
Optional and late: developer plugins do best on HN and Reddit. Needs a tagline under 60 characters, 4+ gallery images and a full day present.

### Dev.to or Hashnode
A how-it-works article: why a history scan matters, how the audit loop works, the eval method including the failed first round. Set the canonical URL to the Pages site if cross-posting.

### Discord and Slack
Only in channels made for sharing (for example a #showcase or #projects channel in Claude Code or AI-tools communities). Short message plus link.

### Awesome lists
awesome-claude-code takes the web issue form only (no PRs) and closes entries under 14 days old or 100 stars. Other lists: read each CONTRIBUTING.md.

### Plugin and skill directories
Claude plugin directory: submit from the repo at claude.ai/directory/manage; the listing reads `plugin.json` and the README; publishing needs a public repo. Codex: no confirmed self-serve directory (UNVERIFIED); users install from the marketplace command. Skill registries such as skills.sh and claude-plugins.dev: check each submission route (UNVERIFIED).

### Newsletters
Changelog News (submit form, own work allowed) and Console.dev (editorial email, developer-first tools). Send after the first week so there is traction to cite.

## Owner approval list

1. Approve each post above, in order, and send it from your own account.
2. Approve each directory or list submission.
3. Nothing in this plan has been posted or submitted.
