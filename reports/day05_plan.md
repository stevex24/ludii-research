# Day 5 — bounded 4×4 NoGo attempt

Run `sh run_day5.sh`. Standard NoGo forbids captures and suicide; the first player without a legal move loses. The solver uses exact minimax, but a resource limit may interrupt it. Only `SOLVED` supports a game-theoretic outcome. Results are saved in `reports/day05_4x4_results.json`.

This is an exploratory runtime benchmark, not a proof that larger boards are intractable. The implementation does not use symmetry reduction or advanced retrograde methods.
