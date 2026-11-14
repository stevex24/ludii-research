# Day 6 Task 5: Statistical Suitability Audit

Candidate pairs: 130
Distinct Ludii paths: 121
Distinct BGG IDs: 129
Complete numeric rating/count pairs: 130
Missing or invalid ratings: 0
Missing or invalid rating counts: 0

## Rating distribution
Minimum: 2.680
Median: 6.320
Mean: 6.202
Maximum: 7.850

## Number of user ratings
Minimum: 30
Median: 133
Maximum: 28745
Pairs with at least 10 user ratings: 130
Pairs with at least 30 user ratings: 130
Pairs with at least 100 user ratings: 77
Pairs with at least 300 user ratings: 43
Pairs with at least 1000 user ratings: 22
Pairs with at least 10000 user ratings: 4

## Duplicate Ludii mappings
Paths with multiple candidate rows: 9
- lud/board/hunt/Coyote.lud: 8172, 317981
- lud/board/race/fill/Camelot.lud: 5251, 14812
- lud/board/race/reach/Jungle.lud: 4031, 6983
- lud/board/race/reach/Santorini.lud: 194655, 9963
- lud/board/space/line/3D Tic-Tac-Toe.lud: 67364, 16387
- lud/board/space/pattern/Kensington.lud: 276459, 2197
- lud/board/space/territory/Lotus.lud: 198525, 2348
- lud/board/space/territory/Virus.lud: 180020, 189351
- lud/board/war/replacement/checkmate/chess/Dragonchess.lud: 23724, 12776

## Duplicate BGG mappings
BGG IDs mapped to multiple Ludii paths: 1
- 93164: lud/board/space/line/Spline+.lud, lud/board/space/line/Spline.lud

## Ludii top-level categories (candidate pairs)
- board: 120
- math: 5
- puzzle: 3
- experimental: 1
- reconstruction: 1

## Leakage and eligibility warnings
- Multiple BGG entries for one Ludii game must stay in the same evaluation group.
- Different variants or related games may share a family even when filenames differ.
- Ludii directory categories are only a preliminary grouping, not verified game families.
- Ratings are historical BGG user averages, not direct measurements of fun.
- No candidate has completed rules verification; training-eligible pairs: 0.
- Do not fit predictive models or claim validation performance from this dataset yet.
