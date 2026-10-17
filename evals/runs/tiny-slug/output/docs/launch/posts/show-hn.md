Status: draft, not posted. Needs owner approval.

# Show HN: outline only (deferred)

HN asks that Show HN text be written by the poster, not generated. This is an outline and a fact sheet; write the final post yourself. Post only after the edge-case eval reads 13/13. Needs: an established HN account, Tuesday to Thursday 8 to 10 AM ET, a few free hours to reply.

## Title idea

Show HN: tiny-slug - a 16-line slugify function for Node.js with no dependencies

## Outline

1. Why you wrote it (your own reason, in your words).
2. What it does: lowercase ASCII slugs, accent stripping, `&` to `and`, custom separator, word-safe `maxLength`.
3. How it works: NFKD normalization, strip combining marks, replace non `[a-z0-9]` runs.
4. What it does not do and when to use slugify, @sindresorhus/slugify or github-slugger instead.
5. What feedback you want.

## Facts you can use (from README Proof and evals/RESULTS.md)

- 16 lines in `index.js`, no runtime dependencies.
- Unit tests: 5 of 5 pass (`npm test`).
- Edge-case eval: 9 of 13 pass as of 2026-10-17 (update after fixes).
- Known gaps: `ß`/`ø` become separators, non-Latin scripts give an empty string, regex-character separators break, `maxLength` on an exact word boundary drops a word.
- Repo: https://github.com/example-dev/tiny-slug
