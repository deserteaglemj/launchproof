# Reddit

Status: draft, not posted. Needs owner approval. Voice pass needed: rewrite in your own words (write-like-me) before posting.

Read each subreddit's sidebar and pinned rules on the day. One subreddit per day. Reply to every comment.

## r/ClaudeAI (Showcase flair if offered)

**Title:** I built a Claude Code plugin that checks your git history and gets a project ready to publish (never pushes for you)

I kept making repos public and then noticing my personal email or home paths in old commits. launchproof is a skill for Claude Code (and Codex) that:

- scans every commit on the branch you will publish for non-noreply emails, personal emails, home paths, 10 secret patterns, .env and key files, and names you mark private
- writes the README (proof, sourced comparison, limitations, FAQ), CONTRIBUTING, SECURITY, CI, llms.txt, AGENTS.md and a Pages page
- scores the repo 0 to 100 and loops until 90+
- drafts a launch plan and posts, and lists every push and post as a command for you to approve

Evals (3 cases, headless, push denied): seeded projects 18.5 and 11.1 to 97.2; a real repo 77.8 to 97.2 but still failing on a private name in its history. Round 1 failed because a same-named command shadowed the skill; that is written up too.

Limit: the score checks structure and evidence, not writing quality.

Repo: https://github.com/deserteaglemj/launchproof (MIT). What would you want it to check?

## r/ClaudeCode

**Title:** Plugin: full-history hygiene scan + launch checklist before you make a repo public

Shorter version of the post above. Lead with the bug I hit while building it: a slash command with the same name as a skill made the Skill tool load the command instead, so the agent never saw the workflow. Fix: drop the command; skills are invocable as /name. Then link the repo.

## r/SideProject (weekly share thread) and r/coolgithubprojects

launchproof: a Claude Code and Codex plugin that scans your git history for personal info and secrets, writes the README and repo files, scores the repo and drafts a launch plan. MIT. https://github.com/deserteaglemj/launchproof
