I ran the launchproof workflow end to end. The audit went from **77.8 to 97.2/100**. The one failure left is `hygiene-history`: a private studio name from your names file is in three old file versions, and those commits are already on `origin/main`. Only a history rewrite and force-push can remove it, so that's your call. Nothing has been pushed, posted, published or committed.

## Score
- **Before:** `score 77.8/100, required failed: ['launch-plan', 'hygiene-history']`
- **After:** `score 97.2/100, required failed: ['hygiene-history']`
- **Remaining failure:** `hygiene-history`: 3 hits for the studio name, in `README.md:156` and `SKILL.md:24` (both the current and the old plugin path), across commits `2b275c3` to `9f68c65`. The current files are clean.
- **Also fixed:** this repo's local `git config user.email` was your personal Gmail address. It's now `191386781+deserteaglemj@users.noreply.github.com`, matching every existing commit. Only this repo's config changed.

## Changed files (all uncommitted)
- **New community files:** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/` (bug, feature, config), `.github/pull_request_template.md`. Each is fitted to this project's rules and commands.
- **Version 0.4.4:**
  - Both `plugin.json` files bumped to 0.4.4, with `homepage` pointing at the landing page.
  - The Codex manifest gained `license` and `keywords`.
  - New `CHANGELOG.md` entry and release notes in `docs/releases/v0.4.4.md`.
- **README:**
  - The comparison is now dated (2026-10).
  - Two FAQ answers added (cost, what to install).
  - New Contributing / Security / License section.
- **Proof:** `evals/RESULTS.md` gained a section on today's re-check (see Pass / Fail below).
- **Discoverability:**
  - `docs/index.html`: the JSON-LD and the visible FAQ now mirror all 13 README FAQ questions, the version is 0.4.4, and `og:image` points at the new card.
  - New `docs/social-preview.html` and its rendered `docs/social-preview.png`.
  - New `docs/launch/repo-metadata.json` with 17 topics.
  - `llms.txt` and `docs/llms.txt` updated, plus small updates to `AGENTS.md` and `docs/launch/LISTINGS.md`.
- **Launch:** `docs/launch/LAUNCH-PLAN.md` and 10 drafts in `docs/launch/posts/`. Show HN is an outline only, since HN asks for hand-written text.

## Pass / Fail / Unproven
- **Pass:**
  - Self-tests: 11 of 11 (`python3 -m unittest discover -s plugins/shotproof/tests -v`, Python 3.14).
  - Manifest JSON check passes, and `claude plugin validate --strict` passes for both the plugin and the marketplace.
  - I re-scored the five HTML eval pages with network blocked: 0.9761, 0.9511, 0.9795, 0.9832 and 0.9298, all matching `results.json`. Cases 06–08 weren't re-run: 08 needs its Vite build, and 06–07 keep their pages out of the repo.
  - The landing page has no sideways scroll at 375px in light or dark mode.
- **Fail:** the history hygiene finding above.
- **Unproven:**
  - Whether the repo is public now. I couldn't run `gh`, and `LISTINGS.md` had claimed "public since 2026-10-17".
  - CI on GitHub.
  - Whether the quickstart works on a clean machine.
  - Search and AI indexing, which takes days.
  - `gitleaks` wasn't run because it isn't installed.
- **Images:** all 30 flagged images are your own fixtures and renders. The two real sites appear only as text scores.

## Owner approval steps, in order
1. **History rewrite.** If the repo was ever public, forks and caches may still hold the old commits.
   ```bash
   git bundle create ../shotproof-before-rewrite.bundle --all
   # ../shotproof-replacements.txt (outside the repo): one "<name>==>the studio" line per name in the names file
   git filter-repo --replace-text ../shotproof-replacements.txt --force
   git remote add origin https://github.com/deserteaglemj/shotproof.git
   uv run python ~/projects/repo-launch-plugin/plugins/launchproof/skills/launchproof/scripts/lp.py hygiene . --rev main --names ../shotproof-names.txt
   ```
2. **Commit, tag and push:**
   ```bash
   git add -A && git commit -m "shotproof 0.4.4: community files, launch prep"
   git tag v0.4.4
   git push --force-with-lease origin main && git push --force origin --tags
   ```
   Without the rewrite, use `git push origin main --follow-tags` instead.
3. **Make it public** if it isn't yet: `gh repo edit deserteaglemj/shotproof --visibility public --accept-visibility-change-consequences`
4. **Description, homepage and topics:** run the `apply_with` command in `docs/launch/repo-metadata.json`.
5. **Pages** (skip if already on): `gh api -X POST repos/deserteaglemj/shotproof/pages -f "source[branch]=main" -f "source[path]=/docs"`
6. **Release:** `gh release create v0.4.4 --title "shotproof v0.4.4" --notes-file docs/releases/v0.4.4.md`
7. **Social preview:** upload `docs/social-preview.png` in Settings > General > Social preview (there's no API for this).
8. **Launch, following the plan's table:**
   - Mon 10-19: Claude plugin directory.
   - Tue 10-20, 8:30 AM ET: Show HN, then X, LinkedIn and Bluesky/Mastodon at noon.
   - Wed 10-21: r/ClaudeAI.
   - Thu 10-22: r/ClaudeCode and Dev.to.
   - Fri 10-23: r/SideProject.
   - Sat 10-24: Discord/Slack.
   - Mon 10-26: r/coolgithubprojects and newsletters.
   - Tue 10-27, 12:01 AM PT: Product Hunt.
   - Sat 10-31: awesome-claude-code, then the other lists as each becomes eligible.