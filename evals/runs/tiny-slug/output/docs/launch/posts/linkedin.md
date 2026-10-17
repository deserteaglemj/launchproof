Status: draft, not posted. Needs owner approval.

Channel: LinkedIn. Needs: owner's account, `docs/demo.png`. Post Tue 2026-10-20, 12:00 PM ET.

---

I just open-sourced a very small thing: tiny-slug, a 16-line JavaScript function that turns any title into a URL slug.

"Crème Brûlée & Café Recipes!" becomes creme-brulee-and-cafe-recipes. No dependencies, a custom separator, and a length limit that cuts at a word.

Before publishing I wrote 13 edge cases with the expected answers fixed up front. It passes 9. The 4 it misses (German ß, non-Latin scripts, regex-character separators, one length bug) are listed in the README, along with the libraries to use when you need them.

Publishing the misses felt more useful than hiding them. Fixes welcome:
https://github.com/example-dev/tiny-slug
