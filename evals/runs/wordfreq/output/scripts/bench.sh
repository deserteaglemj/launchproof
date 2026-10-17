#!/bin/sh
# Usage: scripts/bench.sh [files...]  (defaults to the sample texts in examples/)
if [ "$#" -eq 0 ]; then set -- examples/*.txt; fi
python3 -m wordfreq.cli "$@" -n 20
