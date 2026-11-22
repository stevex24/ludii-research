# Day 1 — Exploratory I/F Scores

## Method

For a game G, define:

B = mean legal moves
D = mean game duration in moves
C = Ludii Balance
S = Ludii DecisionMoves
Q = Ludii Completion

Normalized features:

B* = B / (B + 10)
D* = D / (D + 30)

Strategic-interest proxy:

I(G) = 100 (0.40 B* + 0.30 S + 0.30 C)

Enjoyment-related proxy:

F(G) = 100 (0.25 B* + 0.25 D* + 0.25 C + 0.25 Q)

These are heuristic indices, not validated measurements of
strategic interest or human enjoyment. The coefficients and
normalization constants are design choices, not statistically fitted.
The indices should not be interpreted as human ratings.

## Ember Roads

Game: Ember-Roads-exact-distance-repair.lud
Random-play trials: 200
Seed: 20261121
Maximum moves per trial: 1000

Finished: 200
Capped: 0
Mean legal moves: 8.687581455967232
Mean duration: 26.855
Balance: 0.87
DecisionMoves: 0.9808617016247813
Completion: 1.0

Calculated scores:

I(G) = 74.1 / 100 (rounded to one decimal)
F(G) = 70.2 / 100 (rounded to one decimal)

## Limitations and future work

Random-play features may not describe competent play.
The formulas have not been validated against human judgments.
A larger, verified BGG-Ludii dataset could support statistically
estimated coefficients and out-of-sample validation.
Independent human evaluations would be needed to validate
strategic interest and enjoyment separately.

## Next step

Apply the unchanged formulas to a range of team-designed Ludii
games, then focus research on automatically constructing and
evaluating strong agents for newly designed games.
