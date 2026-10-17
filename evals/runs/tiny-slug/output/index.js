"use strict";
// Turn any string into a URL slug: lowercase, ASCII, words joined by a separator.
function slugify(input, { separator = "-", maxLength = 0 } = {}) {
  let s = String(input)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, separator)
    .replace(new RegExp(`^${separator}+|${separator}+$`, "g"), "");
  if (maxLength > 0 && s.length > maxLength) {
    s = s.slice(0, maxLength).replace(new RegExp(`${separator}[^${separator}]*$`), "");
  }
  return s;
}
module.exports = { slugify };
