const test = require("node:test");
const assert = require("node:assert");
const { slugify } = require("../index.js");

test("basic", () => assert.strictEqual(slugify("Hello, World!"), "hello-world"));
test("accents", () => assert.strictEqual(slugify("Crème Brûlée"), "creme-brulee"));
test("ampersand", () => assert.strictEqual(slugify("R&D"), "r-and-d"));
test("separator", () => assert.strictEqual(slugify("a b", { separator: "_" }), "a_b"));
test("maxLength cuts at a word", () => assert.strictEqual(slugify("one two three", { maxLength: 9 }), "one-two"));
