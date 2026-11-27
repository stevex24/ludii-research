# Ludii Research — Project State

## Objective
Estimate computable game-interest and enjoyment-related features F(G) from Ludii game descriptions and compare them with historical BoardGameGeek ratings. Ratings are noisy proxies, not ground truth for fun.

## Environment
Repository: ~/ludii-research
GitHub: https://github.com/stevex24/ludii-research
Ludii JAR previously used: ~/Downloads/Ludii-1.3.14.jar (verify current location)

## Completed
Days 1–4: KRK, NoGo, Ember Roads validation, initial game measurements.
Day 5: Historical BGG ratings and Ludii game inventory.
Day 6: 130 candidate pairs, with unresolved identity issues.
Day 7: Verification protocol and seven reviewed candidates.
Day 8 Task 1: research/day8/confidence_policy.md
Day 8 Task 2: research/day8/exploratory_dataset.csv

## Day 8 exploratory dataset
Five provisional Level B matches: Santorini 194655, Quarto 681, Pentago 19841, Yavalath 33767, Camelot 5251. Zero strictly verified training pairs.

## Existing feature extractor
Source: ember-roads/measurements/EmberBaseline.java
Uses Ludii GameLoader, MetricsTracker, Balance, Completion, DurationTurns, DecisionMoves.
Reports mean_moves, mean_legal_moves, finished and capped trials.
Arguments: game.lud [trials] [seed].
Uses random moves, a fixed seed and a 1000-move trial cap.

## Current task
Day 8 Task 3: Reuse EmberBaseline.java to measure features for the five exploratory games. First establish the working Java compilation command and actual .lud file paths. Do not rewrite the existing extractor unnecessarily.

## Remaining Day 8 tasks
Task 3: Extract features.
Task 4: Preliminary correlations, only if sufficient matched observations exist.
Task 5: Evaluate limitations and results.
Task 6: Document, commit and push.

## Working rules
One task at a time, approximately two hours per research day.
Prefer single-line Terminal commands and scripts over manual editing.
At each session end, update this file and commit it with the work.
Do not treat title matches as verified game equivalences.
Stage only intended project files.

## Day 8 completion
Five Level B games measured successfully using run_day8.sh (20 trials each, seed 20261115). Results in research/day8/*_baseline.txt and features_and_ratings.csv. Pearson r: branching -0.0501, length -0.2043, balance -0.0038 (n=5). See research/day8/DAY8_REPORT.md. Next: expand verified sample and test measurement stability. Reproduce with ./run_day8.sh followed by python3 research/day8/analyze.py.


## New research plan — Day 2 completed
Exact 3x3 NoGo dataset: 3,884 states.
Training: 3,110; testing: 774.
All validation checks passed.
Report: go/nogo/DAY2_REPORT.md.
Next: Day 3 — static evaluation function.


## New research plan - Day 3 completed
First learned static evaluator implemented.
Training accuracy: 77.88%.
Held-out accuracy: 65.63%.
Mobility baseline: 67.70%.
Depth-3 decision quality: learned 98.43%, mobility 96.26%.
Report: go/nogo/DAY3_REPORT.md.
Next: Day 4 - larger-board transfer and improvements.

## Day 4 — Complete (November 25, 2026)

- Completed four-model feature ablation.
- All four models achieved 99.00% depth-3 decision quality.
- Generated 2000 exactly solved 4x4 positions.
- Measured zero-shot transfer accuracy of 67.40%.
- Implemented time-limited iterative deepening.
- Validated all 3884 reachable 3x3 positions.
- Completed 90 timed search benchmarks.
- Identified BobNoGo as an external benchmark candidate.
- See go/nogo/DAY4_REPORT.md.

## Day 5 — November 26, 2026 — COMPLETE

- Trained nine-feature and five-feature 4x4 models.
- Held-out accuracy: 75.88% and 75.63%.
- Optimized feature extraction: up to 24.40x.
- Validated 7310 feature-extraction positions.
- Implemented depth-aware transposition tables.
- Passed 31072 search validation tests.
- Completed 90 controlled search benchmarks.
- Completed 240 competitive games.
- Mobility led 4x4; Model A led 5x5 overall.
- Relative Elo remains internally calibrated only.
- Full results: go/nogo/DAY5_REPORT.md
