import argparse
import collections
import re
import sys

WORD = re.compile(r"[A-Za-z']+")


def count(text, stop=()):
    words = (w.lower().strip("'") for w in WORD.findall(text))
    return collections.Counter(w for w in words if w and w not in stop)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="wordfreq", description="Print the most common words in text files.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("-n", type=int, default=10, help="how many words to show")
    ap.add_argument("--stop", default="", help="comma-separated words to ignore")
    a = ap.parse_args(argv)
    stop = {s.strip().lower() for s in a.stop.split(",") if s.strip()}
    total = collections.Counter()
    for f in a.files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            total += count(fh.read(), stop)
    for word, n in total.most_common(a.n):
        print(f"{n:6d}  {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
