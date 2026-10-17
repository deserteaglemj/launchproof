I ran launchproof on wordfreq from start to finish. The audit went from 18.5 to **97.2/100**. The one remaining failure is the git history, which leaks private data and can only be fixed by a history rewrite that you have to approve. Nothing was committed, pushed or posted.

## Score
- **Before:** `score 18.5/100, required failed: ['license', 'proof', 'launch-plan', 'hygiene-current', 'hygiene-history']`
- **After:** `score 97.2/100, required failed: ['hygiene-history']`
- **Still failing:** `hygiene-history` has 4 blocking findings, all from commit `2ab3ab6`:
  - a personal author email;
  - the same email as committer;
  - a home path in `scripts/bench.sh`;
  - **an AWS access key in `settings.py`.** The later commit deleted the file, but the key is still in history.

## Changed files (all uncommitted)
- **Code and packaging:**
  - `tests/__init__.py` (new): without it, `unittest discover` ran **0 tests**.
  - `scripts/bench.sh`: removed the home path.
  - `pyproject.toml`: added build system, description, Python ≥3.9, license, keywords and URLs.
  - `.gitignore` (new).
- **Proof and demo:**
  - `evals/cases.json`, `evals/run.py`, `evals/RESULTS.md`
  - `examples/garden.txt`, `examples/harbour.txt` (sample texts I wrote)
  - `scripts/make_demo.py` and `docs/demo.svg`, rendered from a real run
- **Docs:**
  - `README.md` (rewritten), `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
  - `CHANGELOG.md`, `AGENTS.md`, `llms.txt`
  - `docs/releases/v0.3.0.md`
- **GitHub:** `.github/workflows/ci.yml`, issue templates, PR template.
- **Pages:**
  - `docs/index.html`, with structured data for the project and the FAQ
  - `docs/robots.txt`, `docs/sitemap.xml`, `docs/llms.txt`
  - `docs/social-preview.html` and `.png` (1280×640)
- **Launch:** `docs/launch/LAUNCH-PLAN.md`, `docs/launch/repo-metadata.json` (12 topics), and drafts in `docs/launch/posts/` for Show HN, Reddit, X, Bluesky/Mastodon, LinkedIn, Dev.to, Discord, awesome lists and newsletters.

## Pass / Fail / Unproven
- **Pass:**
  - Unit tests: 3/3 with `python3 -m unittest discover -v` (Python 3.9.6).
  - `pip install .` worked in a scratch environment.
  - Working-tree hygiene scan is clean, and the audit scores 97.2.
- **Partial:** evals pass 9/10. The failing case is `café` being counted as `caf` because word matching is ASCII-only. I wrote that expectation before running and kept the case visible as a limitation.
- **Fail:** history hygiene on `main` (needs the rewrite below).
- **Unproven:**
  - CI on GitHub (only run locally).
  - The `pip install git+https://…` quickstart (works only once the repo is public).
  - Search and AI indexing.
  - `claude plugin validate` doesn't apply, since this isn't a plugin.

## Decisions for you
- **Name clash:** `wordfreq` is already a well-known PyPI package (rspeer/wordfreq). The README says they're unrelated, but consider renaming before launch.
- **License holder:** I put `example-dev` as the MIT copyright holder. Replace it with your legal name if you prefer.
- **Python version:** I set the minimum to 3.9 because that is the version I tested, and CI runs on 3.9 only.
- **Leftovers from my run:** `.venv/` came from an accidental `uv run`, and `build/` and `wordfreq.egg-info/` from the install test. All three are git-ignored, so you can delete them.

## Owner approval steps (in order)
```sh
# 1. Rotate the leaked AWS access key in IAM first.
# 2. Commit, back up, rewrite history
git add -A && git commit -m "Prepare v0.3.0 for public release"
git bundle create ../wordfreq-before-rewrite.bundle --all
printf 'Dev Person <1+example-dev@users.noreply.github.com> <%s>\n' "$(git log -1 --format=%ae 2ab3ab6)" > ../mailmap.txt
printf 'regex:/Users/[^/ ]+/corpus==>corpus\n' > ../replacements.txt
git filter-repo --mailmap ../mailmap.txt --replace-text ../replacements.txt --invert-paths --path settings.py --force
python3 lp.py hygiene . --rev main          # expect 0 blocking
# 3. Tag, create repo, push
git tag v0.3.0
gh repo create example-dev/wordfreq --public --source . --remote origin
git push origin main --follow-tags
# 4. Metadata
gh repo edit example-dev/wordfreq --description "Word frequency counter CLI for plain text files: prints the most common words, with stop-word filtering, using only the Python standard library." --homepage "https://example-dev.github.io/wordfreq/" --add-topic word-frequency --add-topic word-count --add-topic word-counter --add-topic text-analysis --add-topic text-processing --add-topic cli --add-topic command-line-tool --add-topic python --add-topic python3 --add-topic stop-words --add-topic corpus-linguistics --add-topic no-dependencies
# 5. Pages
gh api -X POST repos/example-dev/wordfreq/pages -f "source[branch]=main" -f "source[path]=/docs"
# 6. Release
gh release create v0.3.0 --title "wordfreq v0.3.0" --notes-file docs/releases/v0.3.0.md
# 7. Upload docs/social-preview.png in Settings > General > Social preview
```
8. Posts, in the order of `docs/launch/LAUNCH-PLAN.md` (all drafts):

| Date | Channel | Note |
|---|---|---|
| Tue 2026-10-20, 09:00 ET | Show HN | Outline only; HN asks you to write the text yourself |
| Same day | X, Bluesky/Mastodon, LinkedIn | |
| Oct 21–23 | Reddit | r/commandline, then r/Python, then r/coolgithubprojects, one per day |
| Oct 26 | Dev.to | |
| Oct 27 | Discord/Slack | Showcase channels only |
| Nov 2 onward | Newsletters, awesome lists | |

The plan skips Product Hunt and the plugin directories, with a reason for each.