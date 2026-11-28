import csv
import json
import math
import time
from pathlib import Path
from fast_features import fast_extract

root = Path("go/nogo")
N = 5
EPOCHS = 2000
LR = 1.0
L2 = 0.0001

names = (
    "own_mobility",
    "opponent_mobility",
    "own_exclusive",
    "opponent_exclusive",
    "shared_moves",
    "empty_fraction",
    "stone_advantage",
    "liberty_advantage",
    "constrained_advantage"
)

def load(filename):
    data = []

    with (root/filename).open() as f:
        for r in csv.DictReader(f):
            b,w,t = (
                int(r[k]) for k in
                ("black_bits","white_bits","turn")
            )

            x = fast_extract(b,w,t,N)
            y = int(r["winning"])
            data.append((x,y))

    return data

def sigmoid(z):
    if z>=0:
        return 1/(1+math.exp(-z))

    e = math.exp(z)
    return e/(1+e)

def project(data,indices):
    return [
        ((1.0,)+tuple(x[i] for i in indices),y)
        for x,y in data
    ]

def score(weights,x):
    return sum(a*b for a,b in zip(weights,x))

def accuracy(weights,data):
    return sum(
        int(score(weights,x)>=0)==y
        for x,y in data
    )/len(data)

def train(data):
    weights = [0.0]*len(data[0][0])
    count = len(data)

    for epoch in range(1,EPOCHS+1):
        grad = [0.0]*len(weights)

        for x,y in data:
            error = sigmoid(score(weights,x))-y

            for j,value in enumerate(x):
                grad[j] += error*value

        for j in range(len(weights)):
            penalty = L2*weights[j] if j else 0

            weights[j] -= LR*(
                grad[j]/count+penalty
            )

        if epoch%500==0:
            print(
                "Epoch",epoch,
                "accuracy",
                f"{accuracy(weights,data):.2%}",
                flush=True
            )

    return weights

start = time.perf_counter()

training = load("exact_5x5_train.csv")
testing = load("exact_5x5_test.csv")

results = {}

results["majority"] = max(
    sum(y for x,y in testing),
    sum(1-y for x,y in testing)
)/len(testing)

results["mobility"] = sum(
    int(x[0]-x[1]>=0)==y
    for x,y in testing
)/len(testing)

for name in (
    "evaluator_3x3",
    "evaluator_4x4_A",
    "evaluator_4x4_D"
):
    model = json.loads(
        (root/(name+".json")).read_text()
    )

    indices = model.get(
        "feature_indices",
        list(range(9))
    )

    results[name] = accuracy(
        model["weights"],
        project(testing,indices)
    )

for model,indices in (
    ("A",tuple(range(9))),
    ("D",(2,3,4,7,8))
):
    print("\nTRAINING MODEL",model,flush=True)

    train_data = project(training,indices)
    test_data = project(testing,indices)

    weights = train(train_data)

    train_acc = accuracy(weights,train_data)
    test_acc = accuracy(weights,test_data)

    result = {
        "board_size":N,
        "model":model,
        "feature_indices":list(indices),
        "feature_names":[names[i] for i in indices],
        "weights":weights,
        "training_positions":len(training),
        "test_positions":len(testing),
        "training_accuracy":train_acc,
        "test_accuracy":test_acc
    }

    path = root/f"evaluator_5x5_{model}.json"
    path.write_text(json.dumps(result,indent=2)+"\n")

    print("Training accuracy:",f"{train_acc:.2%}")
    print("Test accuracy:",f"{test_acc:.2%}")

    print("\nWeights:")
    for name,value in zip(
        ("intercept",)+tuple(names[i] for i in indices),
        weights
    ):
        print(f"{name:24s} {value:+.6f}")

    results[f"evaluator_5x5_{model}"] = test_acc

print("\nHELD-OUT 5x5 COMPARISON")

for name,value in results.items():
    print(f"{name:24s} {value:.2%}")

(root/"training_5x5_results.json").write_text(
    json.dumps(results,indent=2)+"\n"
)

print("\nTotal seconds:",
      round(time.perf_counter()-start,3))
