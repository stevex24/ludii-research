# Day 1: NoGo rules and test plan

Rules: Players alternate placing a stone on an empty intersection, Black first. Orthogonally adjacent same-color stones form groups. A liberty is an orthogonally adjacent empty intersection. A move is legal only if every group of either color retains at least one liberty afterward. No captures, no suicide, no passing, no ko, no territory scoring. A player without a legal move loses. Board occupancy strictly increases, so a game lasts at most n² moves.

Code: `go/nogo/rules.py` implements neighbors, group liberty validation, legal moves, and play. `go/nogo/test_rules.py` checks empty-board moves, occupied intersections, suicide, capture prohibition, legal placement, and malformed boards.

## Status
Implementation supplied; test results must be recorded after running locally. No `.lud` file has been verified yet. Next: inspect Ludii's built-in NoGo definition and compare sample positions; then implement a memoized exact solver for 3×3.
