import csv
import random
import json
from pathlib import Path
from features import extract, FEATURE_NAMES
from train_evaluator import sigmoid, score

root = Path("go/nogo")

def canonical(b,w,t):
    variants = []
    for reflect in (False,True):
        for rotation in range(4):
            bb = ww = 0
            for i in range(9):
                r,c = divmod(i,3)
                if reflect:
                    c = 2-c
                for _ in range(rotation):
                    r,c = c,2-r
                j = 3*r+c
                if b & (1<<i):
                    bb |= 1<<j
                if w & (1<<i):
                    ww |= 1<<j
            variants.append((bb,ww,t))
    return min(variants)

groups = {}

with (root/"exact_3x3_train.csv").open() as f:
    for r in csv.DictReader(f):
        b,w,t = (int(r[k]) for k in
                 ("black_bits","white_bits","turn"))
        x = extract(b,w,t,3)
        y = int(r["winning"])
        key = canonical(b,w,t)
        groups.setdefault(key,[]).append((x,y))

keys = sorted(groups)
random.Random(20261125).shuffle(keys)

folds = [
    [row for key in keys[i::5]
     for row in groups[key]]
    for i in range(5)
]

models = {
    "A": [],
    "B": ["stone_advantage"],
    "C": ["stone_advantage","empty_fraction"],
    "D": ["stone_advantage","empty_fraction",
          "own_mobility","opponent_mobility"]
}

def select(data,indices):
    return [
        ((1.0,)+tuple(x[j] for j in indices),y)
        for x,y in data
    ]

def train(data,k):
    weights = [0.0]*k
    for epoch in range(2000):
        grad = [0.0]*k
        for x,y in data:
            error = sigmoid(score(weights,x))-y
            for j,v in enumerate(x):
                grad[j] += error*v
        for j in range(k):
            reg = 0.0001*weights[j] if j else 0
            weights[j] -= grad[j]/len(data)+reg
    return weights

results = {}

for name,excluded in models.items():
    indices = [
        i for i,f in enumerate(FEATURE_NAMES)
        if f not in excluded
    ]
    correct = total = 0

    print("\nModel",name,flush=True)
    print("Removed:",excluded,flush=True)

    for i in range(5):
        training = select(
            [row for j,fold in enumerate(folds)
             if j != i for row in fold],indices
        )
        validation = select(folds[i],indices)

        weights = train(training,len(indices)+1)

        c = sum(
            (score(weights,x)>=0)==bool(y)
            for x,y in validation
        )
        correct += c
        total += len(validation)

        print(
            f"Fold {i+1}: "
            f"{100*c/len(validation):.2f}%",
            flush=True
        )

    acc = 100*correct/total
    print(f"Overall: {acc:.2f}%",flush=True)

    results[name] = {
        "excluded": excluded,
        "features": [FEATURE_NAMES[j] for j in indices],
        "cv_accuracy": acc
    }

(root/"ablation_results.json").write_text(
    json.dumps(results,indent=2)
)

print("\nSUMMARY")
for name,r in results.items():
    print(f"Model {name}: {r['cv_accuracy']:.2f}%")
