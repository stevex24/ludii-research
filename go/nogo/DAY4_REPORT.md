# Day 4: Feature Ablation, Transfer and Timed Search

Date: November 25, 2026

## 1. Objectives

- Investigate redundant evaluation features.
- Generate exact training data for larger boards.
- Measure zero-shot transfer between board sizes.
- Implement and validate time-limited alpha-beta search.
- Benchmark search scalability.
- Identify external competitive benchmarks.

## 2. Feature Ablation

Five-fold symmetry-grouped cross-validation:

| Model | Features | Classification | Depth-3 decision quality |
|---|---:|---:|---:|
| A | 9 | 78.14% | 99.00% |
| B | 8 | 75.11% | 99.00% |
| C | 7 | 74.21% | 99.00% |
| D | 5 | 74.73% | 99.00% |

All models preserved 1878 of 1897 forced wins.

Removing redundant features reduced classification
accuracy but did not reduce measured depth-3 decision
quality.

Retain Model A as the baseline and Model D as a
candidate for future experiments.

Model D has not yet been exported as a trained model.

## 3. Exact 4x4 Dataset

- Candidate positions: 25949
- Exactly solved positions: 2000
- Winning positions: 1236
- Losing positions: 764
- Search timeouts: 0
- Solving time: 6.27 seconds
- Sampled plies: 6 through 15

The solving time excludes candidate generation.
The empty 4x4 board remains unsolved by our engine.

## 4. Zero-Shot Transfer

Original 3x3 weights evaluated on 2000 4x4 positions:

- Majority baseline: 61.80%
- Relative mobility: 67.50%
- Learned evaluator: 67.40%

The learned evaluator transferred above the majority
baseline but did not outperform relative mobility.

Prediction accuracy is not equivalent to playing strength.

## 5. Time-Limited Alpha-Beta Search

Implemented:

- Iterative deepening
- Alpha-beta pruning
- Previous-best-move ordering
- Cached legal moves and evaluations
- Explicit terminal recognition
- Return of last completed search result

Exhaustive 3x3 validation:

- Positions: 3884
- Correct proven outcomes: 3884
- Forced wins preserved: 2405/2405
- Errors: 0
- Validation time: 1.878 seconds

## 6. Search Performance

90 benchmark searches completed in 195.25 seconds.

Opening search depth with learned evaluation:

| Board | 0.1s | 1s | 10s |
|---|---:|---:|---:|
| 3x3 | 7 | 7 | 7 |
| 4x4 | 3 | 4 | 6 |
| 5x5 | 2 | 3 | 5 |
| 7x7 | 1 | 2 | 3 |
| 9x9 | 1 | 2 | 2 |

Mobility evaluation generally permits deeper search.

The benchmark uses one sampled position per board
size and game stage. More extensive sampling is needed.

## 7. External Benchmark Candidates

BobNoGo is a historical competitive MCTS-based
NoGo engine and a candidate external benchmark.

University of Alberta NoGo research:
https://webdocs.cs.ualberta.ca/~mmueller/nogo/

Installation and compatibility remain unverified.

No externally calibrated Elo rating has been established.

## 8. Conclusions

Classification accuracy alone is insufficient for
evaluating a static evaluation function.

Exact labels can be generated for sampled larger-board
positions without solving the entire game.

Search scalability is limited by both branching factor
and evaluation cost.

The next research priorities are larger-board training,
faster move generation and feature extraction,
transposition tables, and competitive testing.

The ultimate objective remains a reproducible method
for constructing strong static evaluation functions
for arbitrary games, rather than transferring NoGo
weights directly to unrelated games.

## 9. Limitations

- Random-play sampling may not represent strong play.
- Larger-board exact labels need independent validation.
- Cross-validation search quality is near saturation.
- The current feature extractor computes all nine features.
- Time limits are approximate.
- No full search transposition table is implemented.
- Competitive playing strength remains unmeasured.
- Cross-game method transfer remains untested.
