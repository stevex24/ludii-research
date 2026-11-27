import csv
import json
import math
import time
from pathlib import Path
from features import extract, FEATURE_NAMES

root = Path("go/nogo")

def load_data(name):
    data = []
    with (root/name).open() as f:
        for r in csv.DictReader(f):
            b,w,t,y = (
                int(r[k]) for k in
                ("black_bits","white_bits",
                 "turn","winning")
            )
            data.append((extract(b,w,t,4),y))
    return data

def sigmoid(z):
    if z >= 0:
        return 1/(1+math.exp(-z))
    e = math.exp(z)
    return e/(1+e)

def score(weights,x):
    return sum(w*v for w,v in zip(weights,x))

def project(data,indices):
    return [
        ((1.0,)+tuple(x[i] for i in indices),y)
        for x,y in data
    ]

def accuracy(weights,data):
    return sum(
        (score(weights,x)>=0)==bool(y)
        for x,y in data
    )/len(data)

def train(data,indices):
    data = project(data,indices)
    weights = [0.0]*(len(indices)+1)
    epochs = 2000
    lr = 1.0
    penalty = 0.0001

    for epoch in range(epochs):
        gradient = [0.0]*len(weights)

        for x,y in data:
            error = sigmoid(score(weights,x))-y
            for j,v in enumerate(x):
                gradient[j] += error*v

        for j in range(len(weights)):
            g = gradient[j]/len(data)
            if j:
                g += penalty*weights[j]
            weights[j] -= lr*g

        if (epoch+1)%500 == 0:
            print(
                f"Epoch {epoch+1}: "
                f"{100*accuracy(weights,data):.2f}%",
                flush=True
            )

    return weights

start = time.perf_counter()
training = load_data("exact_4x4_train.csv")
testing = load_data("exact_4x4_test.csv")

models = {
    "A": tuple(range(9)),
    "D": (2,3,4,7,8)
}

original = json.loads(
    (root/"evaluator_3x3.json").read_text()
)["weights"]

results = {}

majority = int(
    sum(y for x,y in training)>=len(training)/2
)

results["majority"] = sum(
    y==majority for x,y in testing
)/len(testing)

results["mobility"] = sum(
    (x[0]-x[1]>=0)==bool(y)
    for x,y in testing
)/len(testing)

results["learned_3x3"] = accuracy(
    original,project(testing,range(9))
)

for name,indices in models.items():
    print(f"\nTRAINING MODEL {name}",flush=True)
    weights = train(training,indices)

    train_acc = accuracy(
        weights,project(training,indices)
    )
    test_acc = accuracy(
        weights,project(testing,indices)
    )

    model = {
        "board_size":4,
        "model":name,
        "feature_indices":list(indices),
        "feature_names":[
            FEATURE_NAMES[i] for i in indices
        ],
        "weights":weights,
        "training_positions":len(training),
        "test_positions":len(testing),
        "training_accuracy":train_acc,
        "test_accuracy":test_acc
    }

    path = root/f"evaluator_4x4_{name}.json"
    path.write_text(json.dumps(model,indent=2))

    results[f"learned_4x4_{name}"] = test_acc

    print(f"Training accuracy: {100*train_acc:.2f}%")
    print(f"Test accuracy: {100*test_acc:.2f}%")
    print("Weights:")
    print(f"  intercept: {weights[0]:+.6f}")

    for i,w in zip(indices,weights[1:]):
        print(f"  {FEATURE_NAMES[i]}: {w:+.6f}")

print("\nHELD-OUT 4x4 TEST RESULTS")
for name,value in results.items():
    print(f"{name:20s}: {100*value:.2f}%")

(root/"training_4x4_results.json").write_text(
    json.dumps(results,indent=2)
)

print("\nTotal seconds:",
      round(time.perf_counter()-start,3))
