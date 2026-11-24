import csv
import json
import time
from pathlib import Path
from features import extract, from_bits, legal_moves
from solve_3x3 import solve

root = Path("go/nogo")
weights = json.loads(
    (root/"evaluator_3x3.json").read_text()
)["weights"]

def moves(b,w,t):
    return sorted(legal_moves(from_bits(b,w,3),t+1,3))

def child(b,w,t,m):
    bit = 1 << m
    if t == 0:
        return b|bit,w,1
    return b,w|bit,0

def mobility(b,w,t):
    return (len(moves(b,w,t))-len(moves(b,w,1-t)))/9

def learned(b,w,t):
    x = (1.0,) + extract(b,w,t,3)
    return sum(a*v for a,v in zip(weights,x))

def search(b,w,t,depth,alpha,beta,evaluate):
    options = moves(b,w,t)

    if not options:
        return -1000.0

    if depth == 0:
        return evaluate(b,w,t)

    best = -float("inf")

    for m in options:
        value = -search(
            *child(b,w,t,m),
            depth-1,-beta,-alpha,evaluate
        )
        best = max(best,value)
        alpha = max(alpha,value)

        if alpha >= beta:
            break

    return best

def choose(b,w,t,depth,evaluate):
    best = -float("inf")
    selected = None

    for m in moves(b,w,t):
        value = -search(
            *child(b,w,t,m),
            depth-1,
            -float("inf"),float("inf"),
            evaluate
        )

        if value > best:
            best = value
            selected = m

    return selected

positions = []

with (root/"exact_3x3_test.csv").open() as f:
    for r in csv.DictReader(f):
        if int(r["winning"]):
            positions.append((
                int(r["black_bits"]),
                int(r["white_bits"]),
                int(r["turn"])
            ))

print("Winning test positions:",len(positions))

for depth in (1,2,3):
    print("\nSearch depth:",depth)

    for name,evaluate in (
        ("Mobility",mobility),
        ("Learned",learned)
    ):
        start = time.perf_counter()
        correct = 0

        for b,w,t in positions:
            m = choose(b,w,t,depth,evaluate)
            opponent_wins,_ = solve(*child(b,w,t,m))
            correct += not opponent_wins

        elapsed = time.perf_counter()-start

        print(
            f"{name:10s}: "
            f"{correct}/{len(positions)} "
            f"({100*correct/len(positions):.2f}%) "
            f"Time: {elapsed:.3f}s"
        )
