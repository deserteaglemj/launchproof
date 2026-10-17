---
name: launchproof
description: Turn a finished project folder into a public-ready GitHub repo and a launch plan, with every claim backed by evidence in the repo. Scans the full git history for personal emails, home paths, secrets, private names and images to review; writes or fixes the README (hero, demo, quickstart, proof with real numbers, honest comparison, limitations, FAQ written as questions people ask AI assistants), LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue and PR templates, CHANGELOG, release notes, CI with a badge, llms.txt, AGENTS.md, a GitHub Pages landing page with JSON-LD, Open Graph, robots.txt and sitemap, repo description and topics, a social preview and plugin or package manifests; scores the result with a checklist and fixes gaps; then drafts a launch plan and posts for Show HN, Reddit, X, LinkedIn, Product Hunt, Dev.to, Discord, awesome lists, plugin directories and newsletters. Never pushes, publishes, posts or submits on its own. Use for "make this repo public", "prepare my project for GitHub", "open source this", "polish my README", "make my repo look professional", "launch my project", "get my repo discovered", "write a launch plan", "is my repo ready to publish", "scan my git history before going public", "release checklist" or "launch posts for Show HN and Reddit".
---

# launchproof

You turn a finished build into a repo people trust, install and can find, then plan its launch. Two rules hold throughout:

- **Evidence over adjectives.** Every number and claim points to a file in the repo. No "first", "only", "best", "fastest", "leading", "state of the art". If you cannot back a claim, cut it.
- **The owner publishes.** Never run `git push`, `gh repo create`, `gh repo edit --visibility public`, `gh release create`, Pages enablement, history rewrites, or post or submit anything. Write those as exact commands in the final report for the owner to approve and run.

**The helper is part of this skill, already on disk:** `LP` = `${CLAUDE_SKILL_DIR}/scripts/lp.py` (Python 3.9+, standard library only). If that variable was not expanded (some hosts), use `scripts/lp.py` inside the base directory this skill was loaded from; if you still cannot see it, find it with `find ~ -path '*launchproof/scripts/lp.py' -not -path '*/node_modules/*' 2>/dev/null | head -1`. Never skip the helper or substitute your own checks for it. Commands show `python3`; if that is missing or blocked by a shim, use any Python 3.9+ (`uv run python`, `/usr/bin/python3`). Exit code 1 from `hygiene` or `audit` means findings, not a crash. Templates are in `${CLAUDE_SKILL_DIR}/templates/`, guides in `${CLAUDE_SKILL_DIR}/references/`; read each guide at the step that names it.

If the request only asks to check or audit ("is my repo ready", "audit"), run steps 0, 1 and 8 read-only, explain each failure and its fix, and change nothing.

**Required outputs, all inside TARGET** (never in a scratch or temp folder): `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, `.github/workflows/<name>.yml`, `llms.txt`, `AGENTS.md`, `docs/index.html`, `docs/robots.txt`, `docs/sitemap.xml`, `docs/social-preview.png`, `docs/launch/repo-metadata.json`, `docs/releases/vX.Y.Z.md`, `docs/launch/LAUNCH-PLAN.md`, `docs/launch/posts/*.md`, and a proof file (for example `evals/RESULTS.md`).

**Done means** `python3 LP audit TARGET --rev <branch>` scores 90 or more and its only required failure, if any, is `hygiene-history` (which needs the owner's approved rewrite). Paste the audit's final `score` line in your report. Do not describe the audit as passing without running it. References in `references/`: read each one at the step that names it.

## 0. Setup

- `TARGET` is the project folder (the argument, else the current directory). Ask for the owner's GitHub username if it is not in the git remote or the request; read it with `gh api user --jq .login` when `gh` is signed in.
- Run `python3 LP facts TARGET` and read the README, manifests, tests, CI and `git log --oneline | head -30`. Write down: name, one-sentence purpose, audience, install path, test command, version, license holder.
- If `TARGET` is not a git repo, say so and continue with file checks; history checks then cover only the working tree.

## 1. Hygiene scan (read `references/hygiene.md`)

1. `python3 LP hygiene TARGET --rev <branch to publish>`. Add `--names FILE` when the owner lists private names (clients, employers, people); keep that file outside the repo. If `gitleaks` is installed, also run `gitleaks git --redact -v TARGET`.
2. Fix working-tree findings directly: relative paths instead of home paths, placeholders instead of emails, delete secrets and add them to `.gitignore`.
3. For history findings, do not rewrite. Write the exact backup (`git bundle create`), rotation and `git filter-repo` commands into the report as an owner-approval step, and set `git config user.email` to the owner's noreply address for new commits.
4. Review every image line: anything that is a third-party logo, a real company's site or an image the owner may not publish gets replaced (generate your own from the project's real output) or flagged.

## 2. Proof

1. Run the project's tests and any evals that exist. Record the command, date, and numbers.
2. If there is no measurable proof, create the smallest honest one: run the test suite and publish pass counts, or a small eval set with fixed pass criteria set before running. Save results to `evals/RESULTS.md` (or the project's existing results file) with the commands to reproduce.
3. Never edit numbers by hand or report a number the files do not contain.

## 3. Scaffold

`python3 LP scaffold TARGET --name NAME --owner OWNER --description "ONE SENTENCE" [--author "Full Name"] [--contact URL-or-email] [--homepage URL]`

It copies only missing files (never overwrites): CONTRIBUTING, CODE_OF_CONDUCT (Contributor Covenant 2.1 by reference), SECURITY, CHANGELOG, issue and PR templates, llms.txt, `docs/index.html`, `docs/robots.txt`, `docs/sitemap.xml`, `docs/social-preview.html`, `docs/launch/repo-metadata.json` and `docs/releases/v0.1.0.md`. Then edit every created file to fit the project: real commands, the real version (rename the release notes file to it), real contact route. Add a LICENSE if missing (MIT unless the owner chose otherwise; holder = owner's name, current year).

## 4. README (read `references/readme.md`)

Rewrite or improve it in the order the reference gives: hero, demo, quickstart, how it works, proof, comparison, limitations, FAQ, contributing/security/license/credits. Keep what the existing README already does well. Make the demo from the real tool on sample content you create.

## 5. Discoverability (read `references/discoverability.md`)

- `docs/launch/repo-metadata.json`: description and 8 to 20 topics.
- `llms.txt` at the root (copy to `docs/llms.txt`), `AGENTS.md` with the exact CI commands.
- `docs/index.html`: title, meta description, canonical, Open Graph, Twitter card, JSON-LD (`SoftwareSourceCode` plus a `FAQPage` mirroring the README FAQ), readable at 375px and in dark mode.
- Social preview: edit `docs/social-preview.html`, then `python3 LP render TARGET/docs/social-preview.html TARGET/docs/social-preview.png`. If no renderer exists, report the one-line install it prints.
- Manifests: if the project is a Claude Code or Codex plugin, make `plugin.json`, `.codex-plugin/plugin.json` and `marketplace.json` complete and in version sync, widen skill descriptions with the phrases people type, and run `claude plugin validate --strict` on the plugin folder and the repo root. For npm or PyPI packages, fill description, keywords, repository, homepage and license.

## 6. CI, changelog, release notes

- `.github/workflows/<name>.yml` running the same test command as AGENTS.md on push and pull_request, with `permissions: contents: read`. Pin actions to major versions (`actions/checkout@v4`). Add its badge to the README: `https://github.com/OWNER/REPO/actions/workflows/<name>.yml/badge.svg`.
- CHANGELOG entry for the release version; `docs/releases/vX.Y.Z.md` with highlights, install, proof numbers and known limitations (it becomes the GitHub release body).
- Run the CI command locally and record the result.

## 7. Launch plan (read `references/launch-channels.md`)

Write `docs/launch/LAUNCH-PLAN.md`:
1. Status line: `Status: draft, not posted or submitted. Every step needs the owner's approval.`
2. Readiness gate with the current audit score and what is still open.
3. A dated sequence table (day, channel, time with timezone, owner action, what it needs).
4. One section per fitting channel: Show HN, Reddit (named subreddits and their rules to re-check), X, LinkedIn, Bluesky or Mastodon, Product Hunt, Dev.to or Hashnode, Discord or Slack, awesome lists, plugin and skill directories (Claude plugin directory, Codex, skill registries), newsletters. Skip a channel only with a one-line reason.
5. Ready-to-paste drafts in `docs/launch/posts/<channel>.md`, each starting with the status line and using only facts from the README proof section. For Show HN, give an outline and facts, and tell the owner to write the final text by hand (HN asks for that).
6. The owner-approval command list (from step 8).

## 8. Audit and fix loop

1. `python3 LP audit TARGET --rev <branch>` (add `--names FILE` if used in step 1).
2. For each FAIL, fix the cause in the files, not the check. Re-run. Stop when the score is 90 or more and the only required failure left, if any, is `hygiene-history`, or after 5 rounds; then report what is still failing and why.
3. Re-read the README and LAUNCH-PLAN once as a skeptical stranger: is every claim backed, is anything private, does the quickstart work as written?

## 9. Report

Reply with:
- **Score**: before and after, and any remaining FAIL lines.
- **Changed files**: grouped list.
- **Pass / Fail / Unproven**: tests run, audit, hygiene (published branch), validate. Search and AI indexing are always unproven at this point (they take days).
- **Owner approval steps**, as exact commands in order: history rewrite (if needed, with backup), `git push origin <branch> --follow-tags`, `gh repo create OWNER/NAME --public --source TARGET --push` or visibility change, `gh repo edit` description, homepage and topics, Pages, `gh release create vX.Y.Z --notes-file docs/releases/vX.Y.Z.md`, social preview upload, then each launch post and submission in plan order.
