#!/bin/sh
set -eu
mkdir -p reports
python -u chess/krk/retrograde.py --solve
