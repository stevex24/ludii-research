import csv
import random
import time
import json
from pathlib import Path
from features import extract,legal_moves,from_bits
from fast_features import fast_extract,fast_extract_D

root = Path("go/nogo")
rng = random.Random(20261126)

def sample_positions(n):
    positions = []

    for game in range(10):
        b,w,t = 0,0,0

        while True:
            positions.append((b,w,t,n))

            options = sorted(
                legal_moves(
                    from_bits(b,w,n),t+1,n
                )
            )

            if not options:
                break

            m = rng.choice(options)

            if t == 0:
                b |= 1<<m
            else:
                w |= 1<<m

            t = 1-t

    return positions

def benchmark(fn,positions,repeats):
    start = time.perf_counter()

    for _ in range(repeats):
        for p in positions:
            fn(*p)

    elapsed = time.perf_counter()-start
    count = repeats*len(positions)

    return {
        "evaluations":count,
        "seconds":elapsed,
        "per_second":count/elapsed,
        "microseconds":1e6*elapsed/count
    }

results = []

print("Board   Original/s    Fast A/s    Fast D/s   A speedup   D speedup")

for n in (3,4,5,7,9):
    positions = sample_positions(n)
    repeats = 10

    old = benchmark(extract,positions,repeats)
    a = benchmark(fast_extract,positions,repeats)
    d = benchmark(fast_extract_D,positions,repeats)

    sa = a["per_second"]/old["per_second"]
    sd = d["per_second"]/old["per_second"]

    print(
        f"{n}x{n} "
        f"{old['per_second']:13.0f}"
        f"{a['per_second']:12.0f}"
        f"{d['per_second']:12.0f}"
        f"{sa:11.2f}x"
        f"{sd:11.2f}x",
        flush=True
    )

    results.append({
        "board_size":n,
        "positions":len(positions),
        "original":old,
        "fast_A":a,
        "fast_D":d,
        "speedup_A":sa,
        "speedup_D":sd
    })

path = root/"fast_features_benchmark.json"
path.write_text(json.dumps(results,indent=2))

print("\nSaved:",path)
