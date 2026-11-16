# Day 8 — Exploratory Game Features and BGG Ratings

## Completed
Five provisional Level B Ludii–BGG matches; 20 random-play trials per game; all 100 trials finished without reaching the 1000-move cap. Reused EmberBaseline.java and created run_day8.sh and analyze.py.

## Pearson correlations (n=5)
- Mean legal moves versus rating: -0.0501
- Mean moves versus rating: -0.2043
- Ludii Balance versus rating: -0.0038

## Limitations
Five observations are insufficient for reliable inference. All game matches remain provisional. BGG aggregate ratings are noisy preference proxies affected by editions, variants, and audiences. Random play differs from competent play. These correlations do not establish causation or predictive validity.

## Next research priority
Expand the independently checked game sample, then rerun the same feature pipeline. Evaluate stability across random seeds and larger trial counts before predictive modeling.

## Reproduction
Run ./run_day8.sh and then python3 research/day8/analyze.py. Requires Java 21 and ~/Downloads/Ludii-1.3.14.jar.
