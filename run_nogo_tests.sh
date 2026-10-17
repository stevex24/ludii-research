#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 go/nogo/test_rules.py
