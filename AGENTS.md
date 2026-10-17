# AGENTS.md

launchproof is a Claude Code and Codex plugin. Its skill takes a finished project folder and makes it public-ready on GitHub (hygiene scan, README with proof, community files, CI, llms.txt, AGENTS.md, Pages, metadata), scores the result, and drafts a launch plan. It never pushes, publishes or posts.

## Install

```bash
claude plugin marketplace add deserteaglemj/launchproof
claude plugin install launchproof@launchproof
```

```bash
codex plugin marketplace add deserteaglemj/launchproof
codex plugin add launchproof@launchproof
```

## Use

- `/launchproof` in a project folder runs the full workflow; "audit this repo for launch" only reports.
- Or ask: "make this repo ready to publish on GitHub".
- The workflow is `plugins/launchproof/skills/launchproof/SKILL.md`. Read it before changing behavior.

## Develop (same commands as CI, `.github/workflows/tests.yml`)

```bash
python3 -m unittest discover -s plugins/launchproof/tests -v
python3 plugins/launchproof/skills/launchproof/scripts/lp.py hygiene . --rev HEAD
python3 plugins/launchproof/skills/launchproof/scripts/lp.py audit . --rev HEAD --min 90
claude plugin validate --strict ./plugins/launchproof
claude plugin validate --strict .
```

Evals (each runs a headless `claude -p` session, about 10 to 25 minutes):

```bash
python3 evals/run_eval.py wordfreq --work /tmp/lp-evals
```

## Layout

- `.claude-plugin/marketplace.json`: marketplace `launchproof`, read by Claude Code and Codex
- `plugins/launchproof/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`: manifests (keep versions in sync with CHANGELOG)
- `plugins/launchproof/skills/launchproof/SKILL.md`: the workflow
- `plugins/launchproof/skills/launchproof/scripts/lp.py`: `facts`, `hygiene`, `scaffold`, `audit`, `render` (standard library only)
- `plugins/launchproof/skills/launchproof/references/`: README, discoverability, hygiene and launch-channel guides
- `plugins/launchproof/skills/launchproof/templates/`: files `scaffold` copies when missing
- `plugins/launchproof/tests/test_lp.py`: self-tests
- `evals/`: `run_eval.py`, `fixtures/`, `results.json`, `RESULTS.md`, `runs/<case>/`
- `docs/`: Pages site, `research/prior-art.md`, `launch/` (plan and draft posts), `releases/`

## Rules for changes

- Every claim in docs links to evidence in the repo. No "first", "only" or "best" (the audit fails them).
- Test strings that look like secrets, emails or home paths are built at runtime so the repo passes its own hygiene scan.
- Bump the version in both manifests and CHANGELOG together.
