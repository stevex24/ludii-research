# Day 4: Comparative Ludii Benchmark

Ludii version: 1.3.14
Trials: 200 per game
Random seed: 20261111
Policy: uniformly random legal moves
Maximum moves per trial: 1000

## Results

| Game | Mean moves | Mean legal moves | DecisionMoves | Completion | Balance |
|---|---:|---:|---:|---:|---:|
| Ember Roads | 27.365 | 8.647 | 0.974 | 1.00 | 0.95 |
| Tic-Tac-Toe | 7.875 | 5.426 | 0.940 | 0.85 | 0.78 |
| NoGo 9x9 | 74.395 | 41.997 | 0.987 | 1.00 | 0.97 |
| Half Chess | 224.510 | 11.465 | 0.989 | 0.12 | 0.98 |

All 200 trials per game terminated without reaching the
1000-move cap.

Ember Roads uses the separately identified repaired version.
NoGo uses Ludii's default 9x9 configuration.

## Verified Ludii metric definitions

Completion:
Fraction of games producing a winner, rather than a draw
or timeout.

Balance:
1 minus the largest difference between players' mean
normalized outcome utilities. For two-player win/draw/loss
games, this equals 1 - abs(W1 - W2) / N.

DecisionMoves:
Mean across games of the fraction of moves made from
positions offering more than one legal move.

## Interpretation

1. High Balance does not imply frequent decisive outcomes.
2. DecisionMoves does not measure strategic importance.
3. Game duration and branching factor are distinct properties.
4. Random-play measurements do not establish game quality,
   optimal-play balance, or human enjoyment.
5. The proposed I(G) and F(G) remain research hypotheses
   requiring operational definitions and human validation.

## Research direction

Compare computational metrics with human evaluations,
test predictive accuracy on held-out games, and investigate
whether optimizing proxy metrics improves actual appeal.

Do not assign arbitrary weights to I(G) or F(G).
