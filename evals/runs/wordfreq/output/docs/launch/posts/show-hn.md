Status: draft, not posted or submitted. Every step needs the owner's approval.

# Show HN (outline only: write the final text by hand, HN asks for that)

Needs: an established HN account, 4 to 6 hours to answer comments, Tue to Thu 08:00 to 10:00 ET.

Title (suggested): `Show HN: wordfreq - count the most common words across text files`
URL: https://github.com/example-dev/wordfreq

## Facts you can use (all from the README)

- `wordfreq FILE... -n N --stop w1,w2` prints the top N words across all files, summed.
- Lower-cases, keeps `don't` as one word, strips quotes, ignores numbers, survives invalid UTF-8.
- Python standard library only, Python 3.9+, MIT.
- 9/10 fixed eval cases pass (`python3 evals/run.py`); the failing one is `café` counted as `caf`.
- Unrelated to the PyPI `wordfreq` package (rspeer), which looks up word frequencies in languages.

## First-comment outline

1. Why you built it (your own words: what you were counting and why `sort | uniq -c` was not enough).
2. How it works in two lines (regex, Counter, sum across files).
3. What is weak: ASCII-only, no stemming, files read into memory.
4. What feedback you want: Unicode word handling without adding dependencies? A default stop list?
5. Say you built it.
