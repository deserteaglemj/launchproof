Status: draft, not posted. Needs owner approval.

Channel: X. Needs: owner's account, `docs/demo.png` attached to post 1. Post Tue 2026-10-20, 9:00 AM ET.

---

1/4
I open-sourced tiny-slug: a 16-line slugify function for Node.js with no dependencies.

"Crème Brûlée & Café Recipes!" → creme-brulee-and-cafe-recipes

[attach docs/demo.png]

2/4
How it works: Unicode NFKD splits é into e + accent, the accents are dropped, & becomes "and", and every other run of non a-z0-9 becomes the separator. Optional custom separator and a maxLength that cuts at a word.

3/4
Numbers: 5/5 unit tests, 9/13 on an edge-case eval I wrote before running it. The 4 misses are real: ß and ø become separators, Japanese/Cyrillic give "", "." as separator breaks, and one maxLength boundary bug. All listed in the README.

4/4
If you need full Unicode, use slugify or @sindresorhus/slugify. If you want something you can read in a minute and vendor, try this. Fixes for the failing cases welcome.

https://github.com/example-dev/tiny-slug
