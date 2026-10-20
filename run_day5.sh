#!/bin/sh
set -eu
python3 go/nogo/solve_4x4_bounded.py --seconds 60 --max-states 300000
