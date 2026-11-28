import csv
import json
import math
import time
from pathlib import Path
from fast_features import fast_extract

root = Path("go/nogo")
N = 5
EPOCHS = 500
LR = 1.0
L2 = 0.0001

def child(b,w,t,m):
    if t==0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

def load(filename):
    positions = []

    with (root/filename).open() as f:
        for r in csv.DictReader(f):
            b,w,t = (
                int(r[k]) for k in
                ("black_bits","white_bits","turn")
            )

            legal = list(map(
                int,r["legal_move_list"].split()
            ))

            good = set(map(
                int,r["winning_move_list"].split()
            ))

            if not 0<len(good)<len(legal):
                continue

            features = {
                m:fast_extract(
                    *child(b,w,t,m),N
                )
                for m in legal
            }

            positions.append(
                (features,good)
            )

    return positions

def make_pairs(positions):
    pairs = []

    for features,good in positions:
        bad = set(features)-good

        for g in sorted(good):
            for b in sorted(bad):
                pairs.append(tuple(
                    x-y for x,y in zip(
                        features[b],features[g]
                    )
                ))

    return pairs

def dot(w,x):
    return sum(a*b for a,b in zip(w,x))

def sigmoid(z):
    if z>=0:
        return 1/(1+math.exp(-z))
    e = math.exp(z)
    return e/(1+e)

def pair_accuracy(w,pairs):
    scores = [dot(w,x) for x in pairs]

    return sum(
        1 if s>1e-12 else
        0.5 if abs(s)<=1e-12 else 0
        for s in scores
    )/len(scores)

def move_accuracy(w,positions):
    total = 0.0

    for features,good in positions:
        scores = {
            m:dot(w,x)
            for m,x in features.items()
        }

        best = min(scores.values())

        tied = [
            m for m,s in scores.items()
            if abs(s-best)<=1e-12
        ]

        total += sum(
            m in good for m in tied
        )/len(tied)

    return total/len(positions)

start = time.perf_counter()

training = load("exact_5x5_train.csv")
testing = load("exact_5x5_test.csv")

train_pairs = make_pairs(training)
test_pairs = make_pairs(testing)

print("Training positions:",len(training))
print("Training pairs:",len(train_pairs))
print("Test positions:",len(testing))
print("Test pairs:",len(test_pairs))

w = [0.0]*9

for epoch in range(1,EPOCHS+1):
    grad = [0.0]*9

    for x in train_pairs:
        error = sigmoid(dot(w,x))-1

        for j,value in enumerate(x):
            grad[j] += error*value

    for j in range(9):
        w[j] -= LR*(
            grad[j]/len(train_pairs)+L2*w[j]
        )

    if epoch%100==0:
        print(
            "Epoch",epoch,
            "pair accuracy",
            f"{pair_accuracy(w,train_pairs):.2%}",
            flush=True
        )

base = json.loads(
    (root/"evaluator_5x5_A.json").read_text()
)

model = dict(base)
model["model"] = "Ranking"
model["weights"] = [0.0]+w
model["objective"] = "pairwise_ranking"

for key in (
    "training_accuracy",
    "test_accuracy",
    "training_positions",
    "test_positions"
):
    model.pop(key,None)

model["training_positions"] = len(training)
model["test_positions"] = len(testing)
model["training_pairs"] = len(train_pairs)
model["test_pairs"] = len(test_pairs)

model["training_pair_accuracy"] = (
    pair_accuracy(w,train_pairs)
)

model["test_pair_accuracy"] = (
    pair_accuracy(w,test_pairs)
)

model["test_move_accuracy"] = (
    move_accuracy(w,testing)
)

(root/"evaluator_5x5_ranking.json").write_text(
    json.dumps(model,indent=2)+"\n"
)

evaluators = {
    "mobility":[1,-1,0,0,0,0,0,0,0]
}

for name in (
    "evaluator_3x3",
    "evaluator_4x4_A",
    "evaluator_4x4_D",
    "evaluator_5x5_A",
    "evaluator_5x5_D",
    "evaluator_5x5_ranking"
):
    m = json.loads(
        (root/(name+".json")).read_text()
    )

    full = [0.0]*9

    for i,value in zip(
        m.get("feature_indices",range(9)),
        m["weights"][1:]
    ):
        full[i] = value

    evaluators[name] = full

random_accuracy = sum(
    len(good)/len(features)
    for features,good in testing
)/len(testing)

results = {
    "random":{
        "pair_accuracy":0.5,
        "move_accuracy":random_accuracy
    }
}

print("\nHELD-OUT MOVE SELECTION")
print("Evaluator                  Pair       Move")

print(
    f"{'random':25s}"
    f"{0.5:9.2%}"
    f"{random_accuracy:11.2%}"
)

for name,weights in evaluators.items():
    p = pair_accuracy(weights,test_pairs)
    a = move_accuracy(weights,testing)

    results[name] = {
        "pair_accuracy":p,
        "move_accuracy":a
    }

    print(f"{name:25s}{p:9.2%}{a:11.2%}")

(root/"ranking_5x5_results.json").write_text(
    json.dumps(results,indent=2)+"\n"
)

print("\nRanking weights:")

for name,value in zip(base["feature_names"],w):
    print(f"{name:24s} {value:+.6f}")

print("\nTotal seconds:",
      round(time.perf_counter()-start,3))
