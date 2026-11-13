# Day 5 Report — Independent Human Ratings for Ludii Games

**Project:** Search in Large Spaces without a Utility Function  
**Date:** 2026-11-12  
**Status:** Dataset discovery, preliminary title matching, and preregistration-style validation plan; **no predictive model trained**.

## Research question

Can inexpensive, reproducible features calculated from formal game rules predict independent human game evaluations well enough to improve the return on investment (ROI) of selecting candidates for human playtesting?

Let \(x(G)\) denote computational measurements for game \(G\), and let \(R(G)\) denote an independently collected BoardGameGeek (BGG) mean user rating. A learned predictor \(\widehat R(G)=f(x(G))\) tests a **proxy** for game appeal; it is **not** a validated intrinsic fun function \(F(G)\). The proposed strategic-interest measure \(I(G)\) remains conceptually distinct.

## Dataset search and accessibility

| Candidate | Human target | Accessibility assessed on Day 5 | Decision / limitation |
|---|---|---|---|
| BoardGameGeek (BGG) | Aggregated player ratings by named game; rating counts | Official rankings page denied access in the user's browser. A public, historical GitHub CSV was successfully downloaded locally. | **Primary exploratory dataset.** Ratings are observational, self-selected, and confounded by reputation, presentation, editions, and audience. |
| Gamefit | Documented enjoyment and pairwise preferences | Application/approval required; data-use restrictions require clarification for predictive-model training. | Potentially strong direct target, **do not train on it without explicit permission**. |
| *Your Move* board-gamer survey | Preferences for mechanics, themes, duration, and other characteristics | Published study/open-data reference; individual raw files not verified here. | Supplementary evidence; not established as per-game labels. |
| Preference Learning Toolbox / Institute of Digital Games | Player-experience judgments, including platformer content | Public dataset directory | Methodological comparison, limited direct mapping to distinct Ludii board games. |
| Zenodo game-quality questionnaires | Human satisfaction and experience | Downloadable spreadsheet files listed | Small set of serious games; limited generalization across Ludii titles. |
| LUDI historical evaluations | Historical human preference judgments | Publication exists; usable original raw judgments not confirmed | Historical prior art, not an established accessible independent test set. |

**Reference URLs** (availability and terms should be rechecked before reuse):

- Official BGG ranks: https://boardgamegeek.com/data_dumps/bg_ranks
- Historical public BGG CSV repository: https://github.com/jalwz17/Board-Game-Data-Analysis
- Historical CSV: https://raw.githubusercontent.com/jalwz17/Board-Game-Data-Analysis/master/bgg_dataset.csv
- Gamefit research guide: https://gamefit.com/research/guide
- Gamefit access: https://gamefit.com/research/apply
- *Your Move* study data reference: https://osf.io/tu8yq
- Preference Learning Toolbox datasets: https://plt.institutedigitalgames.com/datasets.php
- Zenodo game-quality study: https://zenodo.org/records/17816511
- LUDI book: https://doi.org/10.1007/978-1-4471-2179-4

## Reproducible local inventory and matching evidence

Ludii version: **1.3.14**, local JAR `~/Downloads/Ludii-1.3.14.jar`.

- **1,413** `.lud` paths counted in the JAR, saved to `/tmp/ludii_day5_games.txt`.
- Historical BGG CSV downloaded successfully to `/tmp/ludii_bgg.csv` (~2.4 MB).
- **20,344** lines including header; **20,343** BGG records.
- **133** BGG records matched Ludii filenames after case-folding, HTML-unescaping, and removing non-alphanumeric characters.
- **123** distinct Ludii titles matched. **These are preliminary title matches, not verified rule-equivalent games.**
- Naive file-description match ratio: 123 / 1,413 ≈ **8.7%**. This is not a verified proportion of distinct games because `.lud` files may include variants, and matching was not adjudicated.

BGG CSV fields observed: `ID;Name;Year Published;Min Players;Max Players;Play Time;Min Age;Users Rated;Rating Average;BGG Rank;Complexity Average;Owned Users;Mechanics;Domains`.

**Parsing:** semicolon-delimited CSV; decimal comma in `Rating Average` and `Complexity Average`. Convert to numeric with `float(value.replace(',', '.'))` only after validating nonmissing values. Preserve BGG ID as an identifier, not a number to be averaged.

**Examples of plausible title matches:** Chess, Go, Shogi, Xiangqi, Hex, Amazons, Havannah, Yavalath, Quarto, Quoridor, Pentago, Oware, Fanorona, and Hnefatafl.

**Known ambiguity:** Santorini appeared under two BGG IDs; names such as Root, Shogun, Imperial, and Virus may refer to different games/editions. The Day 5 one-liner also displayed trailing periods in Ludii names due to slicing the newline-terminated path before stripping whitespace. The normalized match counts are unaffected by punctuation removal, but the matching code must be corrected before producing a durable mapping. Its dictionary also collapses normalized duplicate Ludii filenames; retain all file paths and inspect collisions in the next pass.

**Data provenance:** The GitHub CSV is a historical snapshot rather than current official BGG data. Its exact collection date and license were not independently verified in the local inspection. Do not redistribute the full dataset without checking rights and attribution. Do not commit downloaded raw CSV automatically.

## Proposed validation protocol (specified before fitting)

### A. Identity and target curation

1. Create a table keyed by **Ludii path + BGG ID**, including exact title, normalized title, BGG mean rating, rating count, and match status.
2. Classify each pair as **verified equivalent rules**, **ambiguous**, or **mismatch**. Exclude ambiguous and mismatched pairs from the primary analysis.
3. Resolve duplicate BGG IDs by *rule equivalence*, not by choosing the highest rating. Keep a documented adjudication trail.
4. Group variants, near-identical implementations, and game families; ensure each group stays entirely in either training or held-out evaluation.
5. Check game count and family count after curation. If too small, label findings exploratory and avoid claims of generalization.

### B. Computational inputs

Begin with the five **Day 4 random-play features** (same definitions and consistent trial policy for all games):

- Mean game length in moves.
- Mean legal-move count.
- `DecisionMoves`: mean proportion of played positions with more than one legal move.
- `Completion`: proportion of trials ending with a winner (not merely terminating).
- `Balance`: `1 - max_{i<j} |mean(normalized_utility_i) - mean(normalized_utility_j)|` across players; draws can produce high Balance.

Day 4 pilot games were Ember Roads, Tic-Tac-Toe, NoGo 9×9, and Half Chess, with 200 random-play trials each. **Their feature measurements are not the 123 matched-game dataset**. Feature extraction for curated matches is future work. Do not silently substitute existing four-game results for missing features.

Document random seeds, Ludii version, trial count, move caps, terminations, missing/failed simulations, and computational cost. Decide whether to include additional features only using training folds or a separately specified hypothesis; avoid retrospective feature shopping.

### C. Out-of-sample design

- Use **nested, group-aware cross-validation**, with outer folds held out by game family; start with five folds if feasible, adjusting only for documented sample/family constraints.
- All scaling, imputation, feature selection, model choice, and regularization tuning occur **within training data**, never on held-out folds.
- Compare training-mean prediction, a simple regularized linear model (ridge), and at most one prespecified small nonlinear alternative if sample size permits.
- Fit feature coefficients from data. **No arbitrary aesthetic weights.**
- Report the number of games and families in each outer fold, and make predictions available for auditing.

### D. Evaluation and uncertainty

- **Prediction:** held-out MAE, RMSE, and Spearman rank correlation, with uncertainty intervals appropriate for clustered/game-family data. Compare against the same-fold training-mean baseline.
- **Rating reliability:** retain `Users Rated`, report sensitivity by rating-count strata, and compare unweighted with a carefully labeled rating-count-weighted sensitivity analysis. Rating counts are not automatically valid inverse-variance weights and are affected by selection bias.
- **Selection ROI:** for prespecified playtesting budgets \(k\), rank only held-out games by predicted rating; compare mean observed ratings of selected top-\(k\) games against random selection of \(k\) from the same held-out pool. Aggregate across folds without leaking held-out ratings into model or feature selection. Use uncertainty intervals and a paired/randomization comparison where feasible.
- **Ablations:** report how removal of each prespecified feature affects held-out performance; do not select a favorable ablation post hoc and call it confirmatory.
- **Sensitivity:** rerun excluding low-confidence identities, low-rating-count games, and potentially mismatched historical editions.

### E. Interpretation and success criteria

A positive result is credible **only if held-out predictions or selection outperform relevant baselines with uncertainty reported**. Inconclusive or negative findings remain informative about the adequacy of these *particular* random-play features and the BGG proxy; they do not establish that computationally estimating fun is impossible. Avoid causal or universal claims. Commercial success, cultural influence, and popularity are not identical to enjoyment of the rules.

## Next work (Day 6 and beyond)

1. Produce a durable, correctly parsed candidate-match CSV **without** overwriting the source or committing raw BGG data; preserve all Ludii paths, BGG IDs, duplicates, and counts.
2. Audit normalized-name collisions and manually verify a manageable sample of high-confidence pairs against rules/editions; record exclusion reasons.
3. Quantify verified matches and independent game families before committing to a model.
4. Estimate the compute cost of extracting the five random-play features for verified matches. Run a small pilot before full batch processing.
5. Freeze the validation plan and baselines **before** examining predictive outcomes.
6. Fit and evaluate only when the curated target table and feature table are complete.

## Day 5 deliverable and limitations

**Delivered:** accessible independent rating source, Ludii catalog inventory, preliminary 123-title overlap, explicit dataset caveats, and a validation design. **Not delivered:** rule-verified 123-game set, per-game computational features, trained predictor, or measured playtesting ROI.

No changes to other project files or Ember Roads source are required for this report.
