# Day 6 Research Report: Ludii–BGG Dataset Curation

## Research objective
Investigate whether computable properties of game descriptions can help select games for human enjoyment studies, using historical BoardGameGeek ratings as an imperfect external proxy rather than as a direct measurement of intrinsic fun.

## Task 1: Title matching
Compared 1,413 Ludii descriptions with 20,343 historical BGG records. Generated 134 candidate pairs representing 124 distinct matched Ludii titles. Exact or normalized title agreement is not proof of rules equivalence.

## Task 2: Ambiguity classification
Classified 108 candidate rows as unique-title candidates, 14 as known ambiguity reviews, and 12 as multiple-BGG candidates. All remained unverified.

## Task 3: Preliminary identity verification
Confirmed mismatches: Root (BGG 237182), Imperial (24181), Shogun (20551), and Unfair (179172). Strong candidates requiring full verification: Jungle (4031) and Camelot (5251). Santorini records 9963 and 194655 require edition/variant review. Remaining 126 pairs are unresolved. These classifications are preliminary, not a complete rules-equivalence audit.

## Task 4: Research dataset
Excluded four confirmed mismatches. Retained 130 candidate pairs representing 121 distinct Ludii paths and 129 distinct BGG IDs. Preserved verification status, evidence notes, rating counts, source identification, and training-exclusion reasons. All 130 records are marked ineligible for training pending verification.

## Task 5: Statistical suitability
All 130 candidate pairs have parseable ratings and rating counts. BGG rating minimum 2.680, median 6.320, mean 6.202, maximum 7.850. Rating-count minimum 30, median 133, maximum 28,745. Candidate pairs with at least 100, 300, 1,000, and 10,000 user ratings: 77, 43, 22, and 4 respectively. Nine Ludii paths have multiple BGG candidates; BGG ID 93164 maps to both Spline and Spline+. Ludii categories: board 120, math 5, puzzle 3, experimental 1, reconstruction 1.

## Methodological limitations
BGG ratings reflect a historical, self-selected population and are not direct measurements of enjoyment. Rating counts vary widely, introducing heterogeneous uncertainty. Game names may be ambiguous, BGG editions may differ from Ludii rules, and variants or families may cause train/test leakage. Ludii directory categories alone do not establish game families. No verified training labels are available; predictive modeling, correlation estimates, and performance claims are premature.

## Day 7 recommendation
Prioritize manual or assisted rules-equivalence verification of high-confidence matches, starting with Jungle and Camelot, and resolve ambiguous BGG editions. Record explicit evidence for every approved mapping. Construct game-family groups before defining held-out evaluation folds. Once a sufficiently large verified sample exists, compare simple baselines and regularized predictors using grouped evaluation, MAE, RMSE, Spearman rank correlation, and top-k candidate-selection benefit with uncertainty intervals.

## Reproducibility
Source: historical BGG CSV used in Day 5 and Ludii 1.3.14 game definitions. Intermediate files include title_matches_unverified.csv, duplicate_title_candidates.csv, title_matches_classified.csv, identity_verification.csv, research_candidates.csv, TASK1_AUDIT.md, TASK4_AUDIT.md, and TASK5_AUDIT.md. Scripts build_research_dataset.py and audit_suitability.py reproduce Tasks 4 and 5 from saved local inputs. Tasks 1–3 used interactive commands and are not yet fully scripted end-to-end.
