import csv
import json
from pathlib import Path
from features import extract

root = Path("go/nogo")

weights = json.loads(
    (root/"evaluator_3x3.json").read_text()
)["weights"]

with (root/"exact_4x4_sample.csv").open() as f:
    rows = list(csv.DictReader(f))

results = {
    "Majority": 0,
    "Mobility": 0,
    "Learned 3x3": 0
}

by_ply = {}

for r in rows:
    b,w,t,y = (int(r[k]) for k in
        ("black_bits","white_bits","turn","winning"))

    x = extract(b,w,t,4)

    predictions = {
        "Majority": True,
        "Mobility": x[0]-x[1]>=0,
        "Learned 3x3": sum(
            a*v for a,v in zip(weights,(1.0,)+x)
        )>=0
    }

    ply = bin(b|w).count("1")

    if ply not in by_ply:
        by_ply[ply] = {
            "total": 0,
            "Mobility": 0,
            "Learned 3x3": 0
        }

    by_ply[ply]["total"] += 1

    for name,prediction in predictions.items():
        correct = int(prediction==bool(y))
        results[name] += correct
        if name != "Majority":
            by_ply[ply][name] += correct

print("ZERO-SHOT TRANSFER: 3x3 -> 4x4")
print("Positions:",len(rows))

for name,c in results.items():
    print(f"{name:15s}: {c}/{len(rows)} "
          f"({100*c/len(rows):.2f}%)")

print("\nAccuracy by ply:")
print("Ply   Positions   Mobility   Learned")

for ply,r in sorted(by_ply.items()):
    n = r["total"]
    print(f"{ply:3d}   {n:9d}   "
          f"{100*r['Mobility']/n:7.2f}%   "
          f"{100*r['Learned 3x3']/n:7.2f}%")

(root/"transfer_4x4_results.json").write_text(
    json.dumps({
        "positions":len(rows),
        "correct":results,
        "by_ply":by_ply
    },indent=2)
)
