# Day 5 — November 26, 2026

## Objective

Improve learned static evaluation functions and
alpha-beta search, and measure competitive strength.

## 1. Reproduction

Day 4 results reproduced successfully.
All 3884 reachable 3x3 positions validated.

## 2. Training on 4x4 positions

2000 exactly labeled sampled positions.
1988 rotational/reflectional symmetry groups.
1602 training positions and 398 test positions.
No symmetry-group overlap.

Held-out prediction accuracy:

| Evaluator | Accuracy |
|---|---:|
| Majority | 62.31% |
| Mobility | 66.58% |
| Learned 3x3 | 67.84% |
| Learned 4x4 A | 75.88% |
| Learned 4x4 D | 75.63% |

Model A retains nine features.
Model D retains five features.
Both use logistic regression with 2000 epochs.

## 3. Feature extraction optimization

Replaced repeated candidate-move flood fills
with a single analysis of groups and liberties.

Expected worst-case complexity reduced from
O(N^2) to O(N), where N is board area,
assuming average constant-time hash operations.

Validated 7310 positions with zero discrepancies.

| Board | Fast A speedup | Fast D speedup |
|---|---:|---:|
| 3x3 | 3.84x | 4.15x |
| 4x4 | 5.46x | 5.70x |
| 5x5 | 7.97x | 8.28x |
| 7x7 | 14.61x | 15.00x |
| 9x9 | 23.39x | 24.40x |

## 4. Transposition tables

Implemented depth-aware exact, lower-bound
and upper-bound entries with move ordering.

Four evaluators tested with and without tables
on all 3884 reachable 3x3 positions.

31072 search tests, zero errors.
All winning moves preserved.

Node reductions ranged from 20.26% to 25.29%.

## 5. Search performance

90 controlled searches using identical positions
and original learned evaluation weights.

One-second opening search depths:

| Board | Original | Fast | Fast+TT |
|---|---:|---:|---:|
| 3x3 | 7 | 7 | 7 |
| 4x4 | 4 | 6 | 7 |
| 5x5 | 3 | 4 | 5 |
| 7x7 | 2 | 3 | 4 |
| 9x9 | 2 | 2 | 3 |

The optimized engine matched or exceeded
original search depth in all 30 comparisons.

## 6. Competitive tournament

240 games, 0.1 seconds per move.
Four agents, six pairings per board size.
Ten random four-ply openings per pairing.
Colors exchanged for each opening.

| Agent | 4x4 wins/60 | 5x5 wins/60 |
|---|---:|---:|
| Mobility | 35 | 30 |
| Learned 3x3 | 25 | 31 |
| Learned 4x4 A | 30 | 33 |
| Learned 4x4 D | 30 | 26 |

Direct relative Elo against mobility:

| Agent | 4x4 | 5x5 |
|---|---:|---:|
| Learned 3x3 | -107.5 | +34.9 |
| Learned 4x4 A | -34.9 | 0 |
| Learned 4x4 D | -34.9 | -34.9 |

Tournament execution time: 152.443 seconds.

## 7. Conclusions

Larger-board training improved held-out
classification accuracy substantially.

Algorithmic optimization improved evaluation
throughput and completed search depth.

Static classification accuracy did not reliably
predict competitive playing strength.

Model A finished first overall on 5x5 without
additional training, but tied mobility directly.

## 8. Limitations

Tournament sample sizes are small.
Relative Elo estimates are not externally calibrated.
Random openings may lead to training positions.
Timing-dependent searches may vary between runs.
Larger-board validation is sample-based.
Search benchmarks use few sampled positions.
No statistically reliable competitive superiority
has yet been established.

## 9. Next steps

Expand competitive testing and investigate
evaluation objectives that better predict
move-selection quality.

Establish stronger external benchmarks and
investigate training on larger-board positions.
