#!/bin/sh
set -eu
mkdir -p reports
python chess/krk/validate_day2.py --solve
