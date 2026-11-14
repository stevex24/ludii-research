# Day 7 — Independent Rules Verification

## Summary
- Candidate records reviewed: 7
- Verification statuses: {'unresolved': 6, 'verified_variant': 1}
- Training-eligible records approved today: 0
- Method: compare Ludii 1.3.14 source against independent rules; do not infer equivalence from titles.

## Candidate findings
- Santorini (BGG 194655): unresolved. Ludii implements two-player 5x5 base Santorini with two workers per side, movement, building, level-three victory and no god powers. Static comparison only; runtime behavior and edition-specific differences remain unverified. BGG aggregate rating may include god-power play. Not training eligible.
- Santorini (BGG 9963): unresolved. Ludii implements two-player 5x5 base Santorini with two workers per side, movement, building, level-three victory and no god powers. Static comparison only; runtime behavior and edition-specific differences remain unverified. BGG aggregate rating may include god-power play. Not training eligible.
- Camelot (BGG 5251): unresolved. Static inspection: 10 men and 4 knights per player; eight-direction steps, canters, captures, compulsory jumps, knight charges and castle occupation are implemented. Historical castle-movement restrictions, stalemate and draw rules need further comparison. No runtime validation. Not training eligible.
- Jungle (BGG 4031): verified_variant. Static source comparison: elephant appears able to capture rat; rat may capture across water boundary; trap rank reduction appears to affect own pieces; only den-entry win is explicit. Runtime behavior not tested. Exclude from training pending further investigation.
- Quarto (BGG 681): unresolved. Standard 4x4 game and sixteen four-attribute pieces; selection and placement match. Full-board draw and declaration rules not explicit.
- Pentago (BGG 19841): unresolved. 6x6 board; four rotations; placement win before rotation is permitted by original rules. Simultaneous lines handled. Full-board draw not explicit.
- Yavalath (BGG 33767): unresolved. Default two-player side-five hex board; four wins and three loses. Swap option present. Confirm published variant and terminal draw handling.

## Next steps
1. Runtime-check Pentago rotation, victory, and draw handling.
2. Resolve Quarto declaration and full-board draw rules.
3. Check Yavalath options against the rated edition.
4. Approve training labels only after documented equivalence checks.
