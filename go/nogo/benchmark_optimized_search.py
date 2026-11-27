import csv
import time
from pathlib import Path
from timed_search import timed_search
from optimized_search import optimized_search

root = Path("go/nogo")

with (root/"timed_search_benchmark.csv").open() as f:
    rows = list(csv.DictReader(f))

positions = {}

for r in rows:
    n = int(r["size"])
    stage = r["stage"]
    b,w,t = (
        int(r[k]) for k in
        ("black_bits","white_bits","turn")
    )
    positions[(n,stage)] = (b,w,t)

results = []
start = time.perf_counter()

print("Board Stage Budget Original Fast Fast+TT")
print("                     Completed depth")

for (n,stage),(b,w,t) in positions.items():
    for budget in (0.1,1.0):
        configurations = (
            ("original",lambda: timed_search(
                b,w,t,n,budget,"learned"
            )),
            ("fast",lambda: optimized_search(
                b,w,t,n,budget,"learned_3x3",False
            )),
            ("fast_tt",lambda: optimized_search(
                b,w,t,n,budget,"learned_3x3",True
            ))
        )

        depths = []

        for name,run in configurations:
            r = run()
            depths.append(r["depth"])

            results.append({
                "size":n,
                "stage":stage,
                "budget":budget,
                "configuration":name,
                "black_bits":b,
                "white_bits":w,
                "turn":t,
                "depth":r["depth"],
                "nodes":r["nodes"],
                "elapsed":r["elapsed"],
                "move":r["move"],
                "score":r["score"],
                "proven":r["proven"],
                "tt_hits":r.get("tt_hits",0)
            })

        print(
            f"{n}x{n} {stage:8s} "
            f"{budget:4.1f} "
            f"{depths[0]:8d}"
            f"{depths[1]:5d}"
            f"{depths[2]:8d}",
            flush=True
        )

path = root/"optimized_search_benchmark.csv"

with path.open("w") as f:
    writer = csv.DictWriter(
        f,fieldnames=list(results[0])
    )
    writer.writeheader()
    writer.writerows(results)

print("\nTotal searches:",len(results))
print("Total seconds:",
      round(time.perf_counter()-start,3))
print("Saved:",path)
