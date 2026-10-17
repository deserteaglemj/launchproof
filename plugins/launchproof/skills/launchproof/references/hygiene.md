# Pre-publish hygiene

A public repo publishes its whole history, not just the last commit. `lp.py hygiene` scans every commit reachable from the refs you name (default: all local refs) plus untracked files:

| Kind | What it finds | Severity |
|---|---|---|
| author-email, committer-email | commit identities that are not a GitHub noreply address | block |
| message-email | addresses in commit messages (Co-Authored-By lines count) | block |
| personal-email | personal-domain addresses in any file version | block |
| home-path | `/Users/<name>`, `/home/<name>`, `C:\Users\<name>` | block |
| aws/github/anthropic/openai/slack/google/stripe keys, private keys, assigned secrets | secrets in any file version | block |
| sensitive-file | `.env`, `*.pem`, `id_rsa`, `credentials.json` and similar | block |
| private-name | names from `--names FILE` (clients, employers, people) | block |
| image-review | every image ever committed | review |

Evidence is masked in the output. If gitleaks is installed, also run `gitleaks git --redact -v .` for a second opinion on secrets (gitleaks, MIT).

## Scan what you will push

Backup tags and old branches stay local, but `--all` sees them. Scan the branch you will publish: `lp.py hygiene . --rev main`. Before pushing, make sure only that branch and its tags go out (`git push origin main --follow-tags`, never `--mirror` or `--all`).

## Fix order

1. **Secrets first: revoke and rotate them** with the issuing service. Rewriting history does not un-leak a secret that was ever pushed anywhere.
2. **Back up** before any rewrite: `git bundle create ../REPO-before-rewrite.bundle --all`.
3. **Rewrite** with git-filter-repo (https://github.com/newren/git-filter-repo, MIT). It rewrites every commit, so do it before the first public push. Ask the owner before running it.
   - Authorship: a `mailmap.txt` with lines `Name <NOREPLY> <old@address>`, then `git filter-repo --mailmap mailmap.txt`.
   - Text (paths, names, emails, secrets): a `replacements.txt` with lines `literal==>replacement` or `regex:pattern==>replacement`, then `git filter-repo --replace-text replacements.txt`. Keep this file outside the repo; it contains the very strings you are removing.
   - Files: `git filter-repo --invert-paths --path path/to/file`.
   - Commit messages: `git filter-repo --replace-message replacements.txt`.
4. **Prevent recurrence**: `git config user.email <ID>+<user>@users.noreply.github.com`, add `.env*` and key files to `.gitignore`, and turn on "Block command line pushes that expose my email" in GitHub email settings.
5. **Re-scan** until the scan reports 0 blocking findings, then review every image line: replace third-party logos, real-site screenshots and stock images you have no license for.

## The noreply address

Find it at GitHub Settings > Emails ("Keep my email addresses private"); it looks like `12345678+username@users.noreply.github.com`. `gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'` prints it.
