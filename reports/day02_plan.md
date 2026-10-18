# Day 2: KRK retrograde analysis

## Ground truth from Day 1
499,968 placements, 399,112 python-chess valid KRK positions, 216 checkmates, 68 stalemates.

## Conventions
Side-to-move win/loss/draw. Rook captures lead to drawn K vs K. No fifty-move or repetition rules. DTM measured in plies, mate is zero. These are computational results, not yet independently verified tablebase values.

## Procedure
1. Run `sh run_day2_sample.sh` and inspect sample successor output.
2. Run `sh run_day2_solve.sh` and save output; can take several minutes and substantial memory.
3. Compare counts with independent reference later; do not publish unverified results as established.
4. Commit code and measured results after reviewing them.

## Caveat
`python-chess` board validity is not a full historical reachability proof. Draws are treated as absorbing terminal outcomes for rook capture and stalemate; unresolved cycles are draws.
