# Day 6: Larger-board training and competitive evaluation

## 1. Exact 5x5 training data

- Generated 30,073 candidate positions.
- Exactly solved 5,000 late-game positions.
- 3,083 winning and 1,917 losing positions.
- Recorded all legal and winning moves.
- Training set: 4,000 positions.
- Test set: 1,000 positions.
- Parent-position symmetries separated across splits.
- One timed-out candidate excluded.

## 2. Static evaluation accuracy

Evaluator             Test accuracy
Majority                 62.90%
Mobility                 71.40%
Learned 3x3              64.90%
Learned 4x4 A            72.70%
Learned 4x4 D            71.10%
Learned 5x5 A            74.50%
Learned 5x5 D            71.30%

Model A uses nine features.
Model D uses five features.

## 3. Pairwise ranking

Trained on 19,909 good/bad move pairs.
Tested on 4,932 pairs across 477 positions.

Evaluator             Pair       Move
Random                50.00%     44.59%
Mobility              74.46%     74.10%
Learned 3x3           75.86%     76.36%
Learned 4x4 A         76.37%     76.87%
Learned 4x4 D         77.08%     77.39%
Learned 5x5 A         76.35%     76.87%
Learned 5x5 D         76.39%     76.03%
Pairwise ranking      76.47%     76.35%

Stone advantage and empty fraction cancel
when comparing sibling positions.

Ranking did not outperform conventional
training in these experiments.

## 4. Competitive tournaments

Seven agents, paired openings, 0.1 seconds
per move, 840 games across two board sizes.

Evaluator             5x5 wins   7x7 wins
Mobility                 75         65
Learned 3x3              49         47
Learned 4x4 A            74         58
Learned 4x4 D            57         59
Learned 5x5 A            58         71
Learned 5x5 D            68         72
Pairwise ranking         39         48

Each agent played 120 games per board size.

On 7x7, learned 5x5 D defeated mobility
15-5, an estimated relative Elo of +190.8.

Both 5x5-trained models topped the 7x7
standings without additional training.

Tournament runtime: 1839.877 seconds.

## 5. External benchmark investigation

BobNoGo remains a candidate external benchmark.
The Fuego SVN endpoint returned HTTP 200.

Required historical revision and patch availability
have not been verified.

Apple C++ tools are installed, but SVN, Homebrew,
Autotools, CMake and Docker are absent.

Installation deferred. No system changes made.

## 6. Limitations

- Exact 5x5 labels lack independent solver validation.
- Training positions are sampled from random play.
- Successor positions may overlap across splits.
- Pairwise training weights positions unequally.
- Static ranking does not override terminal scores.
- Twenty games per pairing limit statistical precision.
- Relative Elo is not externally calibrated.
- New reduced model uses full feature extraction.
- Ranking intercept was arbitrarily fixed at zero.
- Tournament exceeded its estimated runtime.

## 7. Conclusions

Competitive strength cannot reliably be inferred
from static classification accuracy alone.

Larger-board training and reduced feature sets
show promising transfer to larger NoGo boards.

Cross-game generalization remains untested.

Next candidate experiment: standard MCTS as a
reusable competitive baseline and label generator.
