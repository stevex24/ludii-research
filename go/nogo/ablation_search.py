import json
from pathlib import Path
from ablation import folds, models, select, train
from features import extract, FEATURE_NAMES
from solve_3x3 import solve, legal_moves
from functools import lru_cache
from ablation import canonical, keys
import csv

root = Path("go/nogo")

positions = {}

with (root/"exact_3x3_train.csv").open() as f:
    for r in csv.DictReader(f):
        b,w,t = (int(r[k]) for k in
                 ("black_bits","white_bits","turn"))
        if int(r["winning"]):
            positions.setdefault(
                canonical(b,w,t),[]
            ).append((b,w,t))

@lru_cache(None)
def features(b,w,t):
    return extract(b,w,t,3)

def child(b,w,t,m):
    if t == 0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

def search(b,w,t,d,a,z,evaluate):
    options = sorted(legal_moves(b,w,t))

    if not options:
        return -1000.0

    if d == 0:
        return evaluate(b,w,t)

    best = -float("inf")

    for m in options:
        v = -search(
            *child(b,w,t,m),
            d-1,-z,-a,evaluate
        )
        best = max(best,v)
        a = max(a,v)
        if a >= z:
            break

    return best

def choose(b,w,t,evaluate):
    return max(
        sorted(legal_moves(b,w,t)),
        key=lambda m: -search(
            *child(b,w,t,m),2,
            -float("inf"),float("inf"),
            evaluate
        )
    )

results = {}

for name,excluded in models.items():
    indices = [
        j for j,f in enumerate(FEATURE_NAMES)
        if f not in excluded
    ]

    correct = total = 0

    for i in range(5):
        training = select(
            [row for j,fold in enumerate(folds)
             if j != i for row in fold],
            indices
        )

        weights = train(training,len(indices)+1)

        def evaluate(b,w,t):
            x = features(b,w,t)
            return weights[0]+sum(
                weights[k+1]*x[j]
                for k,j in enumerate(indices)
            )

        for key in keys[i::5]:
            for b,w,t in positions.get(key,[]):
                m = choose(b,w,t,evaluate)
                won,_ = solve(*child(b,w,t,m))
                correct += not won
                total += 1

        print(f"Model {name}, fold {i+1} done",
              flush=True)

    acc = 100*correct/total

    results[name] = {
        "correct": correct,
        "total": total,
        "accuracy": acc
    }

    print(f"Model {name}: {correct}/{total} "
          f"({acc:.2f}%)",flush=True)

(root/"ablation_search_results.json").write_text(
    json.dumps(results,indent=2)
)

print("\nSEARCH SUMMARY")
for name,r in results.items():
    print(f"Model {name}: {r['accuracy']:.2f}%")
