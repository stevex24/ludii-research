#!/bin/sh
set -eu
if [ ! -f animation/krk_day3.html ]; then echo 'Run from ludii-research directory' >&2; exit 1; fi
open animation/krk_day3.html
