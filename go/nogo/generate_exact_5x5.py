import csv
import random
import time
from pathlib import Path
from functools import lru_cache
from collections import Counter
from fast_features import analyze
from features import from_bits

root = Path("go/nogo")
N = 5
TARGET = 5000
rng = random.Random(20261127)

class Timeout(Exception):
    pass

deadline = float("inf")

@lru_cache(maxsize=300000)
def moves(b,w,t):
    options,_ = analyze(from_bits(b,w,N),N)
    return tuple(sorted(options[t+1]))

def child(b,w,t,m):
    if t == 0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

@lru_cache(maxsize=500000)
def solve(b,w,t):
    if time.perf_counter() >= deadline:
        raise Timeout

    for m in moves(b,w,t):
        if not solve(*child(b,w,t,m)):
            return True

    return False

start = time.perf_counter()
candidates = set()

print("Generating candidate positions...",flush=True)

for game in range(3000):
    b,w,t = 0,0,0

    while True:
        ply = bin(b|w).count("1")

        if ply >= 13:
            candidates.add((b,w,t))

        options = moves(b,w,t)

        if not options:
            break

        b,w,t = child(
            b,w,t,rng.choice(options)
        )

positions = sorted(candidates)
rng.shuffle(positions)

print("Candidates:",len(positions),flush=True)

rows = []
skipped = 0
distribution = Counter()
solve_start = time.perf_counter()
global_deadline = solve_start+180

for b,w,t in positions:
    if len(rows)>=TARGET:
        break

    if time.perf_counter()>=global_deadline:
        break

    deadline = min(
        time.perf_counter()+0.5,
        global_deadline
    )

    try:
        options = moves(b,w,t)

        winning_moves = [
            m for m in options
            if not solve(*child(b,w,t,m))
        ]

        winning = bool(winning_moves)

        assert winning == solve(b,w,t)

    except Timeout:
        skipped += 1
        continue

    ply = bin(b|w).count("1")
    distribution[ply] += 1

    rows.append({
        "black_bits":b,
        "white_bits":w,
        "turn":t,
        "ply":ply,
        "winning":int(winning),
        "legal_moves":len(options),
        "winning_move_count":len(winning_moves),
        "legal_move_list":" ".join(map(str,options)),
        "winning_move_list":" ".join(
            map(str,winning_moves)
        )
    })

    if len(rows)%500 == 0:
        print(
            "Solved:",len(rows),
            "Skipped:",skipped,
            flush=True
        )

if not rows:
    raise RuntimeError("No positions solved")

path = root/"exact_5x5_sample.csv"

with path.open("w") as f:
    writer = csv.DictWriter(
        f,fieldnames=list(rows[0])
    )
    writer.writeheader()
    writer.writerows(rows)

wins = sum(r["winning"] for r in rows)
terminal = sum(r["legal_moves"]==0 for r in rows)
mixed = sum(
    0<r["winning_move_count"]<r["legal_moves"]
    for r in rows
)

print("\nFINAL RESULTS")
print("Exactly solved:",len(rows))
print("Winning:",wins)
print("Losing:",len(rows)-wins)
print("Terminal:",terminal)
print("Positions with both good and bad moves:",mixed)
print("Skipped:",skipped)

print("\nDistribution by ply:")
for ply,count in sorted(distribution.items()):
    print(ply,count)

print("\nSolver cache:",solve.cache_info())
print("Solving seconds:",
      round(time.perf_counter()-solve_start,3))
print("Total seconds:",
      round(time.perf_counter()-start,3))
print("Saved:",path)
