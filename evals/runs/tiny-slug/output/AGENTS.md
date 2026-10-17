# AGENTS.md

tiny-slug: one dependency-free Node.js function, `slugify(input, { separator, maxLength })`, that turns a string into a lowercase ASCII URL slug.

## Develop

Needs Node.js 22 (what CI uses). No install step: there are no dependencies.

```sh
npm test
node evals/run.js
```

`npm test` is what CI runs (`.github/workflows/ci.yml`). `node evals/run.js` prints the edge-case table; it currently reports 9/13 and is informational, not a CI gate.

## Layout

- `index.js`: the whole library
- `test/slug.test.js`: unit tests (`node:test`)
- `evals/run.js`, `evals/RESULTS.md`: edge-case eval and its recorded results
- `docs/`: GitHub Pages site, release notes, launch plan

## Rules for changes

- Keep zero runtime dependencies.
- Add a unit test for every bug fix. If a fix changes an eval result, re-run `node evals/run.js` and update `evals/RESULTS.md` and the README proof numbers from the real output.
- Keep the version in `package.json`, `CHANGELOG.md` and `docs/releases/` in sync.
- Claims in docs need evidence in the repo. No superlatives.
