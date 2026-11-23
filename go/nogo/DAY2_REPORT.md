# Day 2 — Exact NoGo Dataset

## Results
- Game: standard 3x3 NoGo
- Exact solver: go/nogo/solve_3x3.py
- Starting position: Black wins in 7 plies
- All 9 opening moves are winning
- Reachable states: 3,884

## Dataset
- Exporter: go/nogo/export_3x3.py
- Complete dataset: exact_3x3.csv
- Training: 3,110 positions, 432 symmetry groups
- Testing: 774 positions, 108 symmetry groups
- Split seed: 20261122

## Validation
PASS: 3,884 unique positions.
PASS: Training and testing partition the dataset.
PASS: No symmetry group occurs in both sets.
PASS: All win/loss, DTM and legal-move labels match exact minimax.

## Limitations
Results apply to 3x3 NoGo only.
The split prevents rotation/reflection leakage, but does not
establish generalization to larger boards.
No static evaluator has yet been trained.

## Next session
Train and test a static evaluator using the exact labels.
Measure prediction accuracy and begin evaluating playing strength.
