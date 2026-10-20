#!/bin/sh
set -eu
mkdir -p reports
python3 -m unittest discover -s go/nogo -p 'test_3x3.py' -v
python3 go/nogo/solve_3x3.py | tee reports/day04_results.txt
