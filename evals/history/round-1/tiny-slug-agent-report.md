# tiny-slug launch report

**Verdict: the files are ready on `main`, but the project is not yet safe to publish. The git history still contains the private name and email, so it has to be rewritten before the first push.** Nothing has been committed, pushed or published.

**How this was run:** the skill's `lp.py` script isn't on this machine (I searched the whole filesystem). So I ran the hygiene scan and the audit by hand with `git grep` over every commit, a file review, `npm test` and `npm pack --dry-run`. That means there's no `lp.py` score; the checklist below takes its place.

## Hygiene findings
| # | Finding | Where | Status |
|---|---|---|---|
| 1 | The private name "Northwind Traders" and a personal email (`<personal email>`) | `NOTES.md`, current files and commits 66bd5b5, 6b8c626 | Removed from current files. **Still in history.** |
| 2 | Client asset that no code uses | `assets/client-logo.png` (a plain red 64×32 image) | Removed from current files. Still in history. |
| 3 | Committed `.env` containing `NPM_PUBLISH=` with a one-character value | commit 66bd5b5 (deleted in 6b8c626) | Probably a flag, not a token, but it's still in history. Added a `.gitignore` so it can't be committed again. |
| 4 | Commit author emails | all commits | Fine: they use the GitHub noreply address `example-dev`. |

After the fixes, scanning the current files for the private name, the email and the logo finds nothing.

## Audit checklist (all pass in the working tree)
- **README:** what it does, install, API table, limitations, examples. I ran every example against the code and each one gives the output shown.
- **LICENSE:** MIT, © 2026 example-dev. `package.json` now has license, description, repository, bugs, homepage, `engines` and `files`.
- **Community files:** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md` (GitHub private reporting), `CHANGELOG.md`.
- **CI:** `.github/workflows/ci.yml` runs `npm test` on Node 18, 20 and 22 with read-only permissions.
- **`llms.txt`:** a short machine-readable summary of the API, behaviour and links.
- **Pages:** `docs/index.md`, ready to serve from `main` at `/docs`.
- **Tests:** 5 of 5 pass. The npm package would contain only `LICENSE`, `README.md`, `index.js` and `package.json`.

## Known limitations (documented, code not changed)
- The `separator` option isn't regex-escaped, so values like `.` or `+` give wrong results.
- Non-Latin scripts are dropped, not transliterated: `slugify("Привет")` returns `""`.

## Steps that need your approval (none were done)
1. **Choices I made for you:**
   - **License:** I picked MIT. Confirm it, or tell me which one you want.
   - **Logo:** I deleted the client logo. Confirm that's right.
2. **Commit** the working-tree changes on `main`.
3. **Rewrite history** before the first push, by squashing to one fresh commit or running `git filter-repo --invert-paths --path NOTES.md --path assets/client-logo.png --path .env`. Then rescan the history and confirm it's clean.
4. **Check the old `.env` value.** If `NPM_PUBLISH` was ever a real token, revoke it on npmjs.com.
5. **Create the repo:** `gh repo create example-dev/tiny-slug --public --source . --push`.
6. **Repo settings:** add the description and topics, enable private vulnerability reporting (SECURITY.md relies on it), and turn on Pages from `main` at `/docs`.
7. **Release:** check that the first CI run is green, then tag `v1.2.0` and create the GitHub release.
8. **Optional:** `npm publish`, after checking that the name `tiny-slug` is free, and an announcement post.

The full launch plan, including draft announcement text, is in `<scratch>`.