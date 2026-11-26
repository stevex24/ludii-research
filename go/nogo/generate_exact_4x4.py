import csv
import random
import time
from functools import lru_cache
from pathlib import Path
from features import from_bits, legal_moves

N = 4
rng = random.Random(20261125)
root = Path("go/nogo")

@lru_cache(maxsize=300000)
def moves(b,w,t):
    return tuple(sorted(
        legal_moves(from_bits(b,w,N),t+1,N)
    ))

def child(b,w,t,m):
    if t == 0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

class BudgetExceeded(Exception):
    pass

deadline = float("inf")

@lru_cache(maxsize=300000)
def solve(b,w,t):
    if time.monotonic() >= deadline:
        raise BudgetExceeded

    for m in moves(b,w,t):
        if not solve(*child(b,w,t,m)):
            return True

    return False

positions = set()

for _ in range(3000):
    p = (0,0,0)
    ply = 0

    while True:
        options = moves(*p)

        if ply >= 6:
            positions.add(p)

        if not options:
            break

        p = child(*p,rng.choice(options))
        ply += 1

positions = sorted(positions)
rng.shuffle(positions)

print("Candidate positions:",len(positions))

rows = []
skipped = 0
start = time.monotonic()

for p in positions:
    if len(rows) >= 2000:
        break

    if time.monotonic()-start >= 120:
        break

    deadline = min(
        time.monotonic()+0.5,start+120
    )

    try:
        winning = solve(*p)
    except BudgetExceeded:
        skipped += 1
        continue

    rows.append((*p,int(winning),len(moves(*p))))

    if len(rows)%500 == 0:
        print("Solved:",len(rows),flush=True)

path = root/"exact_4x4_sample.csv"

with path.open("w") as f:
    writer = csv.writer(f)
    writer.writerow([
        "black_bits","white_bits","turn",
        "winning","legal_moves"
    ])
    writer.writerows(rows)

print("\nSolved positions:",len(rows))
print("Winning:",sum(r[3] for r in rows))
print("Losing:",sum(1-r[3] for r in rows))
print("Skipped:",skipped)
print("Seconds:",round(time.monotonic()-start,2))
print("Cache:",solve.cache_info())

print("\nDistribution by ply:")
for ply in range(6,17):
    subset = [
        r for r in rows
        if bin(r[0]|r[1]).count("1")==ply
    ]
    if subset:
        print(ply,len(subset))

print("Saved:",path)
