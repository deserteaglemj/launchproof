"use strict";
// Edge-case eval for slugify. Expected values were fixed before running and
// describe the output a reader would want, not what the code happens to do.
// Run: node evals/run.js
const { slugify } = require("../index.js");

const cases = [
  ["plain words", "Hello, World!", {}, "hello-world"],
  ["accents (French)", "Crème Brûlée", {}, "creme-brulee"],
  ["accents (Spanish)", "Año Niño", {}, "ano-nino"],
  ["ampersand", "Salt & Pepper", {}, "salt-and-pepper"],
  ["extra whitespace", "  many   spaces  ", {}, "many-spaces"],
  ["punctuation only", "!!!", {}, ""],
  ["numbers", "Version 2.0 Release", {}, "version-2-0-release"],
  ["underscore separator", "a b c", { separator: "_" }, "a_b_c"],
  ["maxLength mid-word", "one two three", { maxLength: 9 }, "one-two"],
  ["maxLength on word boundary", "one two three", { maxLength: 7 }, "one-two"],
  ["dot separator", "a b", { separator: "." }, "a.b"],
  ["German sharp s", "Straße", {}, "strasse"],
  ["non-Latin script", "日本語", {}, "日本語"],
];

let pass = 0;
console.log("| Case | Input | Expected | Got | Result |");
console.log("|---|---|---|---|---|");
for (const [name, input, opts, expected] of cases) {
  const got = slugify(input, opts);
  const ok = got === expected;
  if (ok) pass++;
  const o = Object.keys(opts).length ? ` ${JSON.stringify(opts)}` : "";
  console.log(`| ${name} | \`${JSON.stringify(input)}${o}\` | \`${JSON.stringify(expected)}\` | \`${JSON.stringify(got)}\` | ${ok ? "pass" : "FAIL"} |`);
}
console.log(`\n${pass}/${cases.length} cases pass`);
