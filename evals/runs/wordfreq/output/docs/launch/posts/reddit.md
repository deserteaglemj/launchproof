Status: draft, not posted or submitted. Every step needs the owner's approval.

# Reddit

Needs: re-read each sub's sidebar and pinned rules on the day; one sub per day; reply to every comment; attach the demo image as PNG.

## r/commandline (Day 2)

Title: I made a small CLI that prints the most common words across text files

I wanted a one-liner for "what words come up most in these notes" without building a `tr | sort | uniq -c` pipeline each time, so I wrote wordfreq:

    wordfreq notes/*.txt -n 20 --stop the,and,a,of

It lower-cases, keeps contractions like `don't`, strips quotes, ignores numbers, and sums counts across files. Python standard library only.

Honest limit: ASCII letters only, so `café` is counted as `caf`. That is the one failing case out of 10 in the eval set.

Repo: https://github.com/example-dev/wordfreq (I built it; feedback welcome.)

## r/Python (Day 3, Showcase format: re-check required sections)

Title: wordfreq: a dependency-free word frequency CLI (Showcase)

**What my project does:** prints the N most common words across one or more text files, with a stop-word list. `pip install git+https://github.com/example-dev/wordfreq`, then `wordfreq book.txt -n 20`.

**Target audience:** anyone who wants a quick word count from the terminal; a toy-sized tool, not an NLP library.

**Comparison:** `collections.Counter` in your own script gives full control; NLTK's `FreqDist` has real tokenizers and Unicode support; the PyPI `wordfreq` package (unrelated) looks up word frequencies in languages. This one is a ~30-line CLI over `Counter` with no dependencies.

Limit: ASCII-only word pattern (`café` becomes `caf`). 9/10 eval cases pass; that is the failing one. I would like ideas for Unicode words without adding dependencies.

## r/coolgithubprojects (Day 4)

Title: wordfreq - count the most common words across text files (Python, no dependencies)

Link post to https://github.com/example-dev/wordfreq with a comment: what it does in one line, the `--stop` example, the ASCII-only limitation, and that I built it.
