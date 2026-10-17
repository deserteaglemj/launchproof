Status: draft, not posted. Needs owner approval.

Channel: Reddit, one subreddit per day. Re-read each sidebar and pinned rules on the day; say that you wrote it; reply to every comment.

---

## r/node (Wed 2026-10-21, 10:00 AM ET)

Title: I wrote a 16-line slugify for Node with no deps, and an eval showing where it breaks

Body:
tiny-slug turns a string into a lowercase ASCII slug: `slugify("Crème Brûlée & Café Recipes!")` gives `creme-brulee-and-cafe-recipes`. Options: `separator` and a `maxLength` that cuts at a word.

It is NFKD normalize, drop combining marks, `&` to `and`, replace non `[a-z0-9]` runs. That is the whole library.

I wrote 13 edge cases with expected outputs before running them: 9 pass. Misses: `ß`/`ø` become separators, CJK/Cyrillic give an empty string, a `.` separator breaks (unescaped in a regex), and `maxLength` drops a word when the cut lands exactly on a boundary. If you need those, slugify or @sindresorhus/slugify handle them.

Repo and results: https://github.com/example-dev/tiny-slug

Feedback on the failing cases is welcome, especially a small way to handle `ß` without a big character map.

## r/coolgithubprojects (Fri 2026-10-23, 10:00 AM ET)

Title: tiny-slug: 16-line, dependency-free URL slug function for Node.js (with an honest edge-case eval)

Link: https://github.com/example-dev/tiny-slug

First comment: I wrote this. 5/5 unit tests, 9/13 edge cases; the README lists the 4 misses and which libraries handle them.

## r/javascript (Sat 2026-10-24, weekly showcase thread only, if it runs)

Comment: tiny-slug, a 16-line slugify with no dependencies. 9/13 on an edge-case eval, gaps listed in the README: https://github.com/example-dev/tiny-slug
