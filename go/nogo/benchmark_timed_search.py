import csv
import random
import time
from pathlib import Path
from timed_search import timed_search, child
from features import from_bits, legal_moves

root = Path("go/nogo")
rng = random.Random(20261125)

def sample_positions(n):
    history = []
    p = (0,0,0)

    while True:
        b,w,t = p
        options = sorted(
            legal_moves(from_bits(b,w,n),t+1,n)
        )

        if not options:
            break

        history.append(p)
        p = child(*p,rng.choice(options))

    return {
        "opening": history[0],
        "middle": history[len(history)//2],
        "late": history[3*len(history)//4]
    }

rows = []
start = time.perf_counter()

for n in (3,4,5,7,9):
    positions = sample_positions(n)

    for stage,p in positions.items():
        for seconds in (0.1,1,10):
            for evaluator in ("mobility","learned"):
                r = timed_search(
                    *p,n,seconds,evaluator
                )

                row = {
                    "size":n,
                    "stage":stage,
                    "budget":seconds,
                    "evaluator":evaluator,
                    "black_bits":p[0],
                    "white_bits":p[1],
                    "turn":p[2],
                    "ply":bin(p[0]|p[1]).count("1"),
                    **r
                }

                rows.append(row)

                print(
                    f"{n}x{n} {stage:7s} "
                    f"{seconds:4.1f}s "
                    f"{evaluator:8s} "
                    f"depth={r['depth']:2d} "
                    f"nodes={r['nodes']:8d} "
                    f"proven={r['proven']}",
                    flush=True
                )

path = root/"timed_search_benchmark.csv"

with path.open("w") as f:
    writer = csv.DictWriter(
        f,fieldnames=list(rows[0])
    )
    writer.writeheader()
    writer.writerows(rows)

print("\nSUMMARY: LEARNED EVALUATOR")
print("Board   Stage     0.1s    1s   10s")

for n in (3,4,5,7,9):
    for stage in ("opening","middle","late"):
        depths = [
            r["depth"] for r in rows
            if r["size"]==n
            and r["stage"]==stage
            and r["evaluator"]=="learned"
        ]
        print(
            f"{n}x{n}     {stage:7s} "
            + " ".join(f"{d:5d}" for d in depths)
        )

print("\nTotal searches:",len(rows))
print("Total seconds:",
      round(time.perf_counter()-start,2))
print("Saved:",path)
