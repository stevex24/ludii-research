# 262-move pawnless tablebase animation

Open `long_endgame_262.html` in any modern browser. Works offline. Click Play for an accelerating 60-second replay, or use Pause, Restart, End, and the move slider.

**Source:** Frederic Friedel / ChessBase, *Just one of 17,823,400,766 positions* (2015 republication), with the complete 262-move line annotated by Helmut Conrady (2002). https://en.chessbase.com/post/just-one-of-17-823-400-766-positions-2

**Position:** `6N1/5KR1/2n5/8/8/8/2n5/1k6 w - - 0 1`.

**Material:** White K+R+N vs Black K+N+N; no pawns. **Length:** 523 plies (White's 262nd move checkmates).

**Important:** This is a historical tablebase-derived line, not a solution computed by our KRK solver. It exceeds the fifty-move rule and is a theoretical mate line under rules ignoring that draw restriction.

`source_moves.txt` holds the transcribed SAN mainline. `build.py` converts it into `positions.json` while independently checking legal piece movement, capture notation, and king safety. `make_html.py` creates the standalone HTML. No libraries are required to run the animation.

**Timing (presentation version):** The first 20 complete moves take 20 seconds (0.5 seconds per ply). The remaining 483 plies accelerate by linearly shortening each move interval, from about 146 ms to 20 ms, completing in 60 seconds total.
