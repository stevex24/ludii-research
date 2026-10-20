#!/bin/sh
set -eu
mkdir -p reports
python3 go/nogo/validate_3x3.py | tee reports/day04_validation.txt
