# tiny-slug results

Run on 2026-10-17 with Node.js v22.23.1 on macOS, tiny-slug 1.2.0.

## Unit tests

Command: `npm test` (runs `node --test`, the same command CI runs)

- tests: 5
- pass: 5
- fail: 0

## Edge-case eval

Command: `node evals/run.js`

The 13 expected outputs in [run.js](run.js) were written before the first run. They describe the slug a reader would want, so failures are real gaps, not test bugs.

Result: **9/13 cases pass** (4 fail).

| Case | Input | Expected | Got | Result |
|---|---|---|---|---|
| plain words | `"Hello, World!"` | `"hello-world"` | `"hello-world"` | pass |
| accents (French) | `"Crème Brûlée"` | `"creme-brulee"` | `"creme-brulee"` | pass |
| accents (Spanish) | `"Año Niño"` | `"ano-nino"` | `"ano-nino"` | pass |
| ampersand | `"Salt & Pepper"` | `"salt-and-pepper"` | `"salt-and-pepper"` | pass |
| extra whitespace | `"  many   spaces  "` | `"many-spaces"` | `"many-spaces"` | pass |
| punctuation only | `"!!!"` | `""` | `""` | pass |
| numbers | `"Version 2.0 Release"` | `"version-2-0-release"` | `"version-2-0-release"` | pass |
| underscore separator | `"a b c" {"separator":"_"}` | `"a_b_c"` | `"a_b_c"` | pass |
| maxLength mid-word | `"one two three" {"maxLength":9}` | `"one-two"` | `"one-two"` | pass |
| maxLength on word boundary | `"one two three" {"maxLength":7}` | `"one-two"` | `"one"` | FAIL |
| dot separator | `"a b" {"separator":"."}` | `"a.b"` | `""` | FAIL |
| German sharp s | `"Straße"` | `"strasse"` | `"stra-e"` | FAIL |
| non-Latin script | `"日本語"` | `"日本語"` | `""` | FAIL |

## What the failures mean

- `maxLength` drops one word too many when the cut lands exactly on a word boundary.
- The separator is put into a regular expression unescaped, so regex characters such as `.` break it.
- Characters that Unicode normalization does not split into ASCII (`ß`, `ø`, `ł`) become separators.
- Scripts without a Latin form (Japanese, Chinese, Arabic, Cyrillic) produce an empty string.

## Reproduce

```sh
git clone https://github.com/example-dev/tiny-slug.git
cd tiny-slug
npm test
node evals/run.js
```
