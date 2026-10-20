# Day 4: Exact 3×3 NoGo

## Goal
Solve 3×3 NoGo by exhaustive minimax with memoization; report winner, search size, optimal first moves, and an optimal game.

## Rules
Players alternate placing stones on empty vertices. A move is legal only if every connected group of either color has an orthogonally adjacent empty vertex after the placement. No capture, suicide, pass, or removal. A player with no legal moves loses.

## Validation
Run `sh run_day4.sh`. Unit tests cover empty-board legality, suicide, capture prohibition, occupied points, and optimal-line legality. Compare rule semantics with the bundled Ludii `NoGo.lud`; this is a rules comparison, **not** an independent Ludii engine solve. For a true cross-engine comparison, configure a 3×3 Ludii NoGo game and obtain its solver result separately.

## Limits
The state count is memoized states reached by the search, not all mathematically possible arrangements. Tiebreaking selects shortest forced wins and longest forced losses. No 4×4 analysis is attempted today.
