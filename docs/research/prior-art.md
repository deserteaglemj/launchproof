# Prior art

Researched 2026-10-17. Stars, license and last push come from the GitHub API on that day; everything else from each project's own pages. Scores are 1 to 5: Q quality, M maintenance, L license permissiveness (5 = MIT, Apache-2.0, Unlicense or CC0; 1 = no license), F fit for launchproof.

## Candidates

| Project | What it does | Stars | License | Last push | Q | M | L | F |
|---|---|---|---|---|---|---|---|---|
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Official Claude Code plugin directory and manifest examples | 41.5k | Apache-2.0 | 2026-10-17 | 5 | 5 | 5 | 5 |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanner for git history | 30.1k | MIT | 2026-09-30 | 5 | 5 | 5 | 5 |
| [newren/git-filter-repo](https://github.com/newren/git-filter-repo) | Rewrites git history (emails, text, paths) | 13.4k | MIT (per COPYING) | 2026-07-09 | 5 | 4 | 4 | 5 |
| [AnswerDotAI/llms-txt](https://github.com/AnswerDotAI/llms-txt) | The llms.txt format (llmstxt.org) | 2.7k | Apache-2.0 | 2026-09-24 | 4 | 4 | 5 | 5 |
| [agentsmd/agents.md](https://github.com/agentsmd/agents.md) | The AGENTS.md convention for coding agents | 25.0k | MIT | 2026-09-10 | 4 | 4 | 5 | 5 |
| [ossf/scorecard](https://github.com/ossf/scorecard) | Automated supply-chain trust checks for repos | 5.8k | Apache-2.0 | 2026-10-17 | 5 | 5 | 5 | 4 |
| [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template) | README layout template | 16.4k | Unlicense | 2026-04-18 | 4 | 4 | 5 | 4 |
| [github/opensource.guide](https://github.com/github/opensource.guide) | GitHub's Open Source Guides (launching, community) | 15.7k | CC-BY-4.0 | 2026-10-12 | 5 | 5 | 4 | 4 |
| [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) | Secret scanner with live verification | 28.6k | AGPL-3.0 | 2026-10-17 | 5 | 5 | 2 | 4 |
| [coreinfrastructure/best-practices-badge](https://github.com/coreinfrastructure/best-practices-badge) | OpenSSF Best Practices criteria and badge | 1.4k | MIT | 2026-10-15 | 4 | 5 | 5 | 3 |
| [eli64s/readme-ai](https://github.com/eli64s/readme-ai) | Generates READMEs with an LLM API | 3.0k | MIT | 2026-10-14 | 4 | 4 | 5 | 3 |
| [anthropics/skills](https://github.com/anthropics/skills) | Example Agent Skills | 182k | none at repo root | 2026-10-09 | 5 | 5 | 2 | 4 |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Curated list of Claude Code resources | 55.9k | CC BY-NC-ND 4.0 | 2026-10-17 | 5 | 5 | 1 | 5 (as a launch channel) |
| [jessesquires/.github](https://github.com/jessesquires/.github) | Example default community health files | 43 | MIT | 2024-08-14 | 3 | 2 | 5 | 3 |
| [matiassingers/awesome-readme](https://github.com/matiassingers/awesome-readme) | Curated list of good READMEs | 21.6k | none | 2026-10-14 | 3 | 4 | 1 | 2 |
| [kefranabg/readme-md-generator](https://github.com/kefranabg/readme-md-generator) | CLI README generator from package.json | 11.1k | MIT | 2022-09-20 | 3 | 1 | 5 | 2 |
| [libresource/open-source-checklist](https://github.com/libresource/open-source-checklist) | Checklist for releasing open source | 9 | GPL-3.0 | 2024-08-01 | 3 | 1 | 2 | 3 |

Agent skills already on the author's machine that overlap parts of the job (read, not copied): `readme-polish`, `github` (GitHub SEO and GEO), `generative-engine-optimization`, `open-source-strategy`, `new-repo`, and the `launch` and `directory-submissions` skills from coreyhaines31/marketingskills. None of them scans history, scores the result or produces the full set of repo files together; each covers one slice.

## Gap

Each tool covers one slice: README templates (no evidence checks), secret scanners (no emails, home paths or private names, no README), llms.txt and AGENTS.md specs (formats only), Scorecard (supply-chain checks after publishing), launch guides (no repo work). No candidate we found takes a finished folder through history hygiene, evidence-backed docs, agent discoverability files and a launch plan, then scores its own output. That combined workflow is what launchproof adds; the individual pieces are standard and credited below.

## Starting point and what we took

- **Base: anthropics/claude-plugins-official (Apache-2.0).** The plugin layout (`.claude-plugin/plugin.json`, `marketplace.json`, `skills/<name>/SKILL.md`, `commands/`) follows its conventions and `claude plugin validate --strict`. No files copied.
- **Worked example: deserteaglemj/shotproof (MIT, same author).** Its repo is the model for the README order, eval publishing, llms.txt, AGENTS.md and Pages files.
- **gitleaks (MIT) and git-filter-repo (MIT):** not bundled. The skill runs gitleaks when installed and prints git-filter-repo commands for the owner. launchproof's own scanner is a small standard-library fallback that also covers emails, home paths, private names and images, which gitleaks does not target.
- **llms.txt spec (Apache-2.0) and AGENTS.md (MIT):** formats followed; the audit checks the llms.txt structure.
- **Best-README-Template (Unlicense), awesome-readme and opensource.guide (CC-BY-4.0):** ideas for README order and launch steps, rewritten in our own words, credited in `references/readme.md` and here. No text copied.
- **Contributor Covenant 2.1 (CC BY 4.0):** adopted by reference in the CODE_OF_CONDUCT template, with attribution.
- **Not used:** trufflehog (AGPL-3.0; could be invoked as a binary but adds nothing gitleaks lacks for this job), awesome-claude-code text (CC BY-NC-ND), libresource checklist (GPL-3.0).

## Launch-channel sources

The channel facts in `plugins/launchproof/skills/launchproof/references/launch-channels.md` cite their sources inline: the Show HN rules page, the Claude plugin directory submission docs, the awesome-claude-code CONTRIBUTING file, Product Hunt's launch guide, Changelog News and Console.dev. Facts from secondary sources are marked UNVERIFIED there.
