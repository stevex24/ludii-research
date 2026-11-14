# Day 7: Rules-Equivalence Verification Protocol

## Acceptance criteria
1. Confirm game identity using an independent rules source, not title similarity alone.
2. Compare player count, board geometry, equipment, and initial setup.
3. Compare turn structure, legal moves, special moves, and captures.
4. Compare terminal conditions, victory, loss, and draw rules.
5. Identify optional rules, editions, and variants; do not silently merge them.
6. Record source URLs, evidence, discrepancies, and unresolved questions.
7. Approve verified_equivalent only after all essential mechanics are supported by evidence.

## Outcomes
- verified_equivalent: Essential rules agree with documented evidence.
- verified_variant: Related game, but materially different rules or edition.
- mismatch: Different game or incompatible essential rules.
- unresolved: Evidence insufficient.

## Research safeguards
BGG ratings are historical user averages, not direct measures of fun. Preserve BGG IDs and rating counts. Keep related games and duplicate labels in the same evaluation group. Never promote a candidate automatically.

## Reference documentation
https://ludii.games/downloads/LudiiGameLogicGuide.pdf
https://boardgamegeek.com/wiki/page/Versions_Guidelines
