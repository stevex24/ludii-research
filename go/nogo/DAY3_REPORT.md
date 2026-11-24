# Day 3 - First Learned Static Evaluator

## Implementation
Implemented nine board-size-independent features using
flood fill, group liberties, mobility and exclusive moves.
Empty-board tests passed on 3x3, 5x5 and 7x7 boards.

## Validation
All 3,884 exact positions tested.
PASS: Legal move agreement with exact solver.
PASS: Rotation invariance.
PASS: Reflection invariance.
PASS: Color-exchange invariance.

2,708 positions (69.72%) have different legal move
sets for Black and White.

## Training
Logistic regression using standard Python.
Training positions: 3,110.
Features: 9 plus intercept.
Epochs: 2,000.
Training accuracy: 77.88%.

## Held-out prediction accuracy
Test positions: 774.
Majority baseline: 65.63%.
Mobility baseline: 67.70%.
Learned evaluator: 65.63%.

## Evaluation speed
Mobility: 50,034 evaluations/sec.
Learned: 43,522 evaluations/sec.
Learned evaluation takes approximately 15% longer.

## Alpha-beta decision quality
508 held-out winning positions.
Percentage of moves preserving a forced win:

Depth   Mobility   Learned
1       90.75%     89.76%
2       93.50%     92.91%
3       96.26%     98.43%

At depth 3:
Mobility: 489 correct, 19 errors, 0.143 seconds.
Learned: 500 correct, 8 errors, 0.171 seconds.
Decision errors reduced by 57.9%.

## Preliminary conclusion
Standalone classification accuracy does not necessarily
predict decision quality when combined with search.

The learned evaluator outperformed mobility at depth 3,
but not at depths 1 and 2.

## Limitations
Small board, single dataset split, fixed search depths.
No equal-time comparison or competitive Elo established.
Transfer to larger boards remains untested on nonempty
positions. Further independent testing is needed.

## Next session
Investigate larger-board transfer, improved training
methods and search performance under equal time budgets.
