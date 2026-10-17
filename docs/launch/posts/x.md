# X thread (also Bluesky and Mastodon)

Status: draft, not posted. Needs owner approval. Voice pass needed: rewrite in your own words (write-like-me) before posting.

1/ I built launchproof: a Claude Code and Codex plugin that takes a finished project and makes it safe and ready to publish on GitHub, then plans the launch. It never pushes or posts for you. github.com/deserteaglemj/launchproof

2/ Step one scans every commit you are about to publish: non-noreply author emails, personal emails, home folder paths, secrets, .env files and names you list as private. Deleted files count too.

3/ Then it writes the README (with proof and limitations), community files, CI, llms.txt, AGENTS.md and a Pages page, and scores the repo 0 to 100 until it passes 90. [attach assets/scores.png]

4/ Evals: two seeded projects went from 18.5 and 11.1 to 97.2. A real repo went 77.8 to 97.2 and still fails: a private name sits in its public history, and only the owner can rewrite that.

5/ Limit: the score checks structure and evidence, not how well the README reads. Method and the failed first round are in evals/RESULTS.md. Feedback welcome.
