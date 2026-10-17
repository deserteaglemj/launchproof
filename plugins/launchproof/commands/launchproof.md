---
description: Make a finished project public-ready on GitHub (hygiene scan, README, community files, CI, llms.txt, Pages, launch plan), scored and fixed until it passes
argument-hint: "[project folder] [audit] [owner <github-user>] [names <file>]"
---

Use the `launchproof` skill from this plugin and follow it end to end, including the audit-and-fix loop and the final report.

Request: $ARGUMENTS

- The project folder is the first path in the request, else the current directory.
- `audit` means report only: run `lp.py hygiene` and `lp.py audit`, explain each failure and the fix, and change nothing.
- `owner <user>` sets the GitHub owner. `names <file>` passes a private-names list to the hygiene scan.
- Never push, publish, post or submit. List those steps for the owner to approve.
