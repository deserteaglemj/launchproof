# Eval results

- Date: 2026-10-17
- Python: 3.9.6 on Darwin
- Command: `python3 evals/run.py` (this file is written by that command; do not edit by hand)
- Criteria: A case passes when the CLI exits 0 and its stdout equals `expected` exactly. Expectations were written before the first run and are not changed to match output.
- Result: **9/10 cases passed**

| Case | Result | Output |
|---|---|---|
| `case-merge` | pass | `3  apple` |
| `stop-words` | pass | `1  cat /      1  hat` |
| `stop-case-insensitive` | pass | `(empty)` |
| `contraction-kept` | pass | `2  don't` |
| `quotes-stripped` | pass | `2  hello` |
| `multi-file-sum` | pass | `2  b` |
| `limit-n` | pass | `1  x /      1  y` |
| `digits-ignored` | pass | `1  apples` |
| `invalid-utf8-no-crash` | pass | `2  ok` |
| `accented-word` | FAIL | `2  caf` |
