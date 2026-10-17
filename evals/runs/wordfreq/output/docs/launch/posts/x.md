Status: draft, not posted or submitted. Every step needs the owner's approval.

# X thread

Needs: demo image as PNG (export docs/demo.svg), post after Show HN on Day 1.

1/ I built wordfreq: a small CLI that prints the most common words across text files. Python standard library only. [demo image]

2/ `wordfreq notes/*.txt -n 20 --stop the,and,a,of` sums counts across files, lower-cases, keeps "don't" as one word and ignores numbers.

3/ 10 fixed eval cases, 9 pass. The failing one is honest: "café" is counted as "caf" because the word pattern is ASCII-only.

4/ Not the PyPI wordfreq package (that one looks up word frequencies in languages). MIT licensed: https://github.com/example-dev/wordfreq
