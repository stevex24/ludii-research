# Day 3 — KRK optimal-play animation

## Source and status
The 32-ply UCI line and initial FEN come from the Day 2 user-verified output. The animation reproduces that fixed line; it does not solve chess or compute DTM itself.

Start FEN: `8/8/8/8/8/8/1Rk5/K7 b - - 0 1`
Final FEN: `8/8/8/8/8/4K3/8/4k1R1 b - - 32 17`

## Playback
Open `animation/krk_day3.html` in a browser. Play lasts approximately 30 seconds, using 32 linearly decreasing inter-move intervals, normalized to total 30 seconds. Controls: Play, Pause, Previous, Next, Reset.

## Validation checklist (not yet performed on user's Mac)
- [ ] Browser opens local HTML without network
- [ ] First position has white king a1, rook b2, black king c2, black to move
- [ ] 32 moves are shown in order and the final position is white king e3, rook g1, black king e1
- [ ] Final move is Rg1# and DTM reaches 0
- [ ] Playback lasts approximately 30 seconds and accelerates
- [ ] Pause/replay/step controls work

## Caveats
The underlying solver omits 50-move and repetition draw rules. The visual animation is an artistic presentation of an optimal line, not an experimentally validated measure of beauty or interestingness. The JavaScript updates the board on discrete moves; it does not interpolate moving pieces.

## Day 3 schedule
0–20 install/open; 20–45 verify positions; 45–70 check timing and controls; 70–95 discuss choreography; 95–110 record observations; 110–120 Git commit.
