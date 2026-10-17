I ran the launchproof skill end to end on tiny-slug. The audit went from **11.1 to 97.2/100**, and the only check still failing is `hygiene-history`, which needs your approved history rewrite. Nothing was committed, pushed, created or posted; all changes are uncommitted in the working tree.

## Score
- **Before:** `score 11.1/100, required failed: ['readme', 'license', 'proof', 'launch-plan', 'hygiene-current', 'hygiene-history']`
- **After:** `score 97.2/100, required failed: ['hygiene-history']`
- **Remaining FAIL:** `hygiene-history — 4 blocking finding(s) in git history or commit metadata`. These are:
  - a `.env` file holding an npm publish token (`NPM_PUBLISH`), committed in 66bd5b5 and deleted in 6b8c626;
  - `NOTES.md` with a personal email and the private client name;
  - a `Co-Authored-By` line in commit 66bd5b5 with a client person's email;
  - `assets/client-logo.png`, an image to review (a red rectangle called "client logo"), which I removed.

## Changed files
- **Removed:** `NOTES.md` (private name and email) and `assets/client-logo.png` (a client image, never referenced).
- **Added:**
  - **Hygiene:** `.gitignore` (`.env*`, `*.pem`, `node_modules/`). I also set the local `git config user.email` to `1+example-dev@users.noreply.github.com`; it was your personal Gmail.
  - **Proof:** `evals/run.js` (13 edge cases, expected outputs written before running) and `evals/RESULTS.md`.
  - **Docs:** `README.md`, `LICENSE` (MIT, Dev Person 2026), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md` (1.2.0), `AGENTS.md`, `llms.txt` (also copied to `docs/llms.txt`).
  - **GitHub:** `.github/workflows/ci.yml`, `.github/ISSUE_TEMPLATE/*` and `.github/pull_request_template.md`.
  - **Site:** `docs/index.html` (JSON-LD for the project and the FAQ), `docs/robots.txt`, `docs/sitemap.xml`, `docs/demo.html` and `docs/demo.png`, `docs/social-preview.html` and `docs/social-preview.png` (1280×640).
  - **Launch:** `docs/releases/v1.2.0.md`, `docs/launch/repo-metadata.json` (12 topics), `docs/launch/LAUNCH-PLAN.md`, and drafts in `docs/launch/posts/` (show-hn, x, bluesky-mastodon, linkedin, reddit, devto, discord, newsletters).
- **Edited:** `package.json` now has description, keywords, repository, homepage, license, bugs and `files`, plus an `eval` script. The version stays 1.2.0.

## Pass / Fail / Unproven
- **Pass:**
  - `npm test`: 5/5 pass on Node v22.23.1.
  - Audit: 97.2.
  - Hygiene on the current files: 0 blocking.
  - Both PNGs rendered and looked correct.
- **Fail:**
  - Hygiene on the published branch's history: 4 blocking (above).
  - The new edge-case eval: **9/13 pass**. `ß` gives `stra-e`, Japanese/Chinese text gives `""`, a `.` separator gives `""`, and `maxLength` drops a word when the cut lands exactly on a word boundary. The README publishes all four as limitations; I didn't change `index.js`.
- **Not applicable:** `claude plugin validate`, because this is not a plugin. gitleaks isn't installed, so it wasn't run.
- **Unproven:** CI on GitHub, the GitHub-install quickstart (it needs the repo public), and search/AI indexing (takes days).

## Owner approval steps (in order)
```sh
# 0. Revoke the npm token that was in .env (npmjs.com > Access Tokens). Rewriting history does not un-leak it.

# 1. Back up and rewrite history (git-filter-repo is installed)
git bundle create ../tiny-slug-before-rewrite.bundle --all
git filter-repo --force --invert-paths --path .env --path NOTES.md --path assets/client-logo.png
git filter-repo --force --replace-message <scratch>
uv run python ~/projects/repo-launch-plugin/plugins/launchproof/skills/launchproof/scripts/lp.py hygiene . --rev main --names ../tiny-slug-names.txt   # expect 0 blocking

# 2. Commit and tag
git add -A && git commit -m "Prepare tiny-slug 1.2.0 for public release"
git tag -a v1.2.0 -m "tiny-slug 1.2.0"

# 3. Create the repo and push only main
gh repo create example-dev/tiny-slug --public --source . --remote origin
git push origin main --follow-tags

# 4. Description, homepage, topics
gh repo edit example-dev/tiny-slug --description "URL slug generator for Node.js: a 16-line, dependency-free slugify function that turns any string into a lowercase ASCII slug, with custom separator and word-safe max length." --homepage "https://example-dev.github.io/tiny-slug/" --add-topic slug --add-topic slugify --add-topic slug-generator --add-topic url-slug --add-topic permalink --add-topic seo --add-topic nodejs --add-topic javascript --add-topic string-manipulation --add-topic zero-dependency --add-topic unicode --add-topic diacritics

# 5. Pages
gh api -X POST repos/example-dev/tiny-slug/pages -f "source[branch]=main" -f "source[path]=/docs"

# 6. Release
gh release create v1.2.0 --title "tiny-slug v1.2.0" --notes-file docs/releases/v1.2.0.md

# 7. Upload docs/social-preview.png in Settings > General > Social preview
```
The replacements file sits outside the repo because it contains the strings being removed.

**8. Posts, in plan order**, as set out in `docs/launch/LAUNCH-PLAN.md`:

| Date | Channel |
|---|---|
| Tue 2026-10-20 | X, Bluesky/Mastodon (9 AM ET), LinkedIn (12 PM ET) |
| Wed 2026-10-21 | r/node |
| Thu 2026-10-22 | Dev.to |
| Fri 2026-10-23 | r/coolgithubprojects |
| Sat 2026-10-24 | r/javascript showcase thread |
| Tue 2026-10-27 | Discord/Slack |
| From Mon 2026-11-02 | Newsletters |

Some channels are deliberately not in the sequence:
- **Show HN** is held until the eval reads 13/13, and you'd write that post by hand.
- **Awesome lists** are held until the project has real users.
- **Product Hunt and plugin directories** are skipped, each with a one-line reason in the plan.