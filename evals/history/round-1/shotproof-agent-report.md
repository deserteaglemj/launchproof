# launchproof report: shotproof (deserteaglemj/shotproof, `main`)

**The project is close to public-ready, with one blocker: the private names are still in git history, and that history is already on GitHub.** I couldn't follow the launchproof skill exactly. Its instructions and its `lp.py` helper aren't installed anywhere on this machine, so `lp.py hygiene` and `lp.py audit` never ran and there's no launchproof score. I ran the same checks by hand instead, which means each item below is pass/fail, not scored.

## Hygiene
| Check | Result |
|---|---|
| Private names (2 entries), current files | **None found** |
| Private names, git history | **Found in 4 places across 2 commits.** Commit `2b275c3` (screenshot-to-code 0.2.0) added them to `README.md` and `SKILL.md`. Commit `5e876f9` (0.4.1) removed them from the files, but they stay in history. |
| Already pushed? | **Yes.** Local `main` is the same commit as `origin/main` (`d25ebf5`), so this history is on GitHub. |
| Names in commit authors or messages | None. Both author emails are GitHub noreply addresses. |
| Secrets, API keys, private keys | None |
| Local paths (`/Users/…`, etc.) | None |
| Emails | Only placeholders (`you@example.com`, `maya@example.com`) |
| Image metadata | Not checked: the command was denied. |
| Third-party material | The two real-site cases (Hacker News, GOV.UK) are correctly kept out by `.gitignore`. |

## Readiness
- **Claims:** the scores in the README, landing page, `llms.txt` and CHANGELOG all match `evals/RESULTS.md`. "first", "only" and "best" never appear as claims.
- **Tests:** all 11 self-tests pass. The three manifests parse, and both `plugin.json` files say 0.4.3.
- **CI, `llms.txt`, Pages:** all present and correct. CI has read-only permissions, the root and `docs/` copies of `llms.txt` are identical, and the landing page has canonical, Open Graph and JSON-LD tags plus `robots.txt` and `sitemap.xml`.
- **Community files:** missing, so I added them.

## Changes made (not committed)
- `SECURITY.md`: tells people to report privately through GitHub's vulnerability reporting.
- `CONTRIBUTING.md`: setup, the test command and the rules for changes, all taken from AGENTS.md. It sets no new review policy.
- `.github/ISSUE_TEMPLATE/bug_report.yml` and `config.yml`, which links security reports to the private form.
- `.github/pull_request_template.md`
- `.github/dependabot.yml`: monthly updates for GitHub Actions.
- `CHANGELOG.md`: an "Unreleased" entry. There are no plugin changes, so no version bump.
- `AGENTS.md`: updated the line that said there was no CONTRIBUTING file.

After the changes, all the YAML files parse and none of the new or edited files contain the names.

## Steps that need your approval
1. **Decide what to do about the names in history.** Either accept that they're exposed, or rewrite history (for example `git filter-repo --replace-text`) and force-push `main`. If you rewrite, also ask GitHub Support to purge cached views of the old commits, and expect any existing forks or clones to keep the old history.
2. Commit and push the community files to `main`.
3. Turn on private vulnerability reporting (Settings → Code security). `SECURITY.md` and the issue-template link depend on it.
4. Optional: add a code of conduct. It needs a contact for enforcement, so I didn't choose one for you.
5. In repo settings: set the description, website (`https://deserteaglemj.github.io/shotproof/`), topics and social preview (`assets/social-preview.png`). Make sure Pages is serving from `main` `/docs`.
6. Before a release, run `claude plugin validate --strict ./plugins/shotproof` and `claude plugin validate --strict .`
7. Directory listings in `docs/launch/LISTINGS.md` are still drafts. awesome-claude-code is eligible from 2026-10-31. The skills directory is not eligible yet.

I didn't push, post, create repos or rewrite history. To get the real launchproof audit and score, install the launchproof plugin so its skill and `lp.py` are on disk, then re-run it.