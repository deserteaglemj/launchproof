Status: draft, not posted or submitted. Every step needs the owner's approval.

---
title: Counting words is harder than it looks: a 30-line CLI and its 10 eval cases
tags: python, cli, opensource, beginners
canonical_url: https://github.com/example-dev/wordfreq
---

Needs: Dev.to account; check tag popularity on the day.

## The problem

"Which words come up most in these files?" sounds like `split()` plus a counter. Then you hit `The` vs `the`, `don't`, `'quoted'` words, numbers, and a file with a broken byte in it.

## What wordfreq does

```sh
pip install git+https://github.com/example-dev/wordfreq
wordfreq notes/*.txt -n 20 --stop the,and,a,of
```

1. Read each file as UTF-8, replacing invalid bytes.
2. Find runs of `[A-Za-z']+`, lower-case them, strip edge quotes.
3. Drop stop words (case-insensitive) and sum counts across files with `collections.Counter`.

## Testing it honestly

I wrote 10 cases in `evals/cases.json` with exact expected output before running them. Result: 9/10 pass (`python3 evals/run.py`, see `evals/RESULTS.md`).

The failure: `café café` prints `2  caf`. The pattern is ASCII-only. I left the case in, failing, so the limitation stays visible.

## Limitations

- ASCII letters only; hyphenated words split; no stemming.
- Files are read fully into memory.
- Unrelated to the PyPI `wordfreq` package, which looks up word frequencies in languages.

Code and evals: https://github.com/example-dev/wordfreq (I am the author.)
