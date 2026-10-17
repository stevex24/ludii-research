# KRK tablebase research — Day 1 results

Date: 2026-10-17

## Observed results

Command: `python chess/krk/enumerate.py`

```
{'placements': 499968, 'legal': 399112, 'stalemate': 68, 'checkmate': 216}
Example checkmate: 8/8/8/8/8/R7/8/k1K5 b - - 0 1
```

## Interpretation

- Raw enumerated states: 64 × 63 × 62 × 2 = 499,968.
- 399,112 pass `python-chess` board validity checks.
- 216 are classified as checkmate and 68 as stalemate.
- These are enumerator outputs, not retrograde tablebase results.
- The state model currently omits history-dependent draw rules and does not yet incorporate transitions to king-versus-king after rook capture.

## Next task

Implement legal successor enumeration, capture-to-draw handling, and retrograde win/draw/loss classification, then DTM.
