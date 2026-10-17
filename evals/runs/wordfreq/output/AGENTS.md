# AGENTS.md

wordfreq: a standard-library-only Python CLI that prints the most common words in text files.

## Develop

Same commands CI runs (`.github/workflows/ci.yml`):

```sh
python3 -m unittest discover -v
python3 evals/run.py
pip install . && wordfreq examples/*.txt -n 3
```

`evals/run.py` rewrites `evals/RESULTS.md`; it exits 0 even when a case fails, so read its last line (`N/M cases passed`). One case (`accented-word`) is a known failure.

## Layout

- `wordfreq/cli.py`: `count()` and the `main()` entry point (the whole tool)
- `tests/`: unittest tests for `count()`
- `evals/cases.json`: fixed eval cases; `evals/run.py`: runner
- `examples/`: sample texts used by the demo and smoke test
- `scripts/make_demo.py`: regenerates `docs/demo.svg` from a real run
- `docs/`: GitHub Pages site, release notes and launch drafts

## Rules

- No third-party runtime dependencies.
- Keep the version equal in `pyproject.toml`, `wordfreq/__init__.py` and `CHANGELOG.md`.
- Never edit numbers in `evals/RESULTS.md` or the README proof section by hand; rerun `python3 evals/run.py`.
- Do not change an eval expectation to make it pass; fix the code or add a new case.
