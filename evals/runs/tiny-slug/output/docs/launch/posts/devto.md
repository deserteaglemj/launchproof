Status: draft, not posted. Needs owner approval.

Channel: Dev.to (or Hashnode). Needs: owner's account; set the canonical URL to the GitHub README if cross-posting. Tags (check on the day): javascript, node, opensource, webdev. Publish Thu 2026-10-22, 9:00 AM ET.

---

# A URL slug function in 16 lines, and the 4 cases it gets wrong

I needed URL slugs for titles like "Crème Brûlée & Café Recipes!" and wanted code I could read in full, so I wrote [tiny-slug](https://github.com/example-dev/tiny-slug). Disclosure: I am the author.

## The whole idea

```js
String(input)
  .normalize("NFKD")                 // é -> e + combining accent
  .replace(/[̀-ͯ]/g, "")   // drop the accents
  .toLowerCase()
  .replace(/&/g, " and ")
  .replace(/[^a-z0-9]+/g, separator) // everything else becomes the separator
```

Then trim separators from the ends, and if `maxLength` is set, cut and drop the trailing partial word.

```js
slugify("Crème Brûlée & Café Recipes!");                       // "creme-brulee-and-cafe-recipes"
slugify("Hello, World!", { separator: "_" });                  // "hello_world"
slugify("How to write a tiny slug library", { maxLength: 20 }); // "how-to-write-a-tiny"
```

## Testing it honestly

Besides 5 unit tests (all pass), I wrote 13 edge cases with the expected output fixed before the first run. Result: 9 of 13.

The misses:

- `"Straße"` gives `"stra-e"`: NFKD does not split `ß`, so it becomes a separator. Same for `ø`, `ł`, `æ`.
- `"日本語"` gives `""`: no Latin form, so nothing survives.
- `separator: "."` gives `""`: the separator goes into a `RegExp` unescaped.
- `maxLength: 7` on `"one two three"` gives `"one"`: when the cut lands exactly on a boundary, the "drop the partial word" step drops a whole word.

All of them are in [evals/RESULTS.md](https://github.com/example-dev/tiny-slug/blob/main/evals/RESULTS.md), reproducible with `node evals/run.js`.

## When to use something else

If your input includes German, Nordic, Polish or non-Latin text, use [slugify](https://github.com/simov/slugify) (character map, locales) or [@sindresorhus/slugify](https://github.com/sindresorhus/slugify) (transliteration). For GitHub-style heading anchors, use [github-slugger](https://github.com/Flet/github-slugger).

The three smaller bugs are good first PRs if you want one.
