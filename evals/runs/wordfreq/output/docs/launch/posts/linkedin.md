Status: draft, not posted or submitted. Every step needs the owner's approval.

# LinkedIn (optional, low fit)

Needs: demo image as PNG.

I kept writing the same `sort | uniq -c` pipeline to see which words come up most in a folder of notes, so I turned it into a small open-source tool: wordfreq.

`wordfreq notes/*.txt -n 20 --stop the,and,a,of` prints the top words across every file. It uses only the Python standard library.

I wrote 10 eval cases with fixed expectations before running them. 9 pass. The one that fails is worth knowing: accented words like "café" are counted as "caf", because the word pattern is ASCII-only. That is the next thing to fix.

MIT licensed: https://github.com/example-dev/wordfreq
