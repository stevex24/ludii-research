import csv
import json
import math
from pathlib import Path
from features import extract, FEATURE_NAMES

ROOT = Path("go/nogo")

def sigmoid(z):
    if z >= 0:
        return 1/(1+math.exp(-z))
    e = math.exp(z)
    return e/(1+e)

def load_data(filename):
    data = []
    with (ROOT / filename).open() as f:
        for r in csv.DictReader(f):
            x = extract(
                int(r["black_bits"]),
                int(r["white_bits"]),
                int(r["turn"]), 3
            )
            y = int(r["winning"])
            data.append(((1.0,) + x, y))
    return data

def score(weights, x):
    return sum(w*v for w,v in zip(weights,x))

def accuracy(weights, data):
    return sum(
        (score(weights,x) >= 0) == bool(y)
        for x,y in data
    ) / len(data)

def main():
    data = load_data("exact_3x3_train.csv")
    weights = [0.0]*(1+len(FEATURE_NAMES))
    rate = 1.0
    penalty = 0.0001
    epochs = 2000

    for epoch in range(epochs):
        grad = [0.0]*len(weights)

        for x,y in data:
            error = sigmoid(score(weights,x))-y
            for j,v in enumerate(x):
                grad[j] += error*v

        for j in range(len(weights)):
            reg = penalty*weights[j] if j else 0
            weights[j] -= rate*(grad[j]/len(data)+reg)

        if (epoch+1) % 500 == 0:
            print(
                "Epoch", epoch+1,
                "Training accuracy:",
                round(100*accuracy(weights,data),2)
            )

    model = {
        "training_board_size": 3,
        "features": ["intercept"]+list(FEATURE_NAMES),
        "weights": weights,
        "epochs": epochs,
        "learning_rate": rate,
        "regularization": penalty
    }

    (ROOT / "evaluator_3x3.json").write_text(
        json.dumps(model, indent=2)
    )

    print("\nLearned coefficients:")
    for name,w in zip(model["features"],weights):
        print(f"{name:25s} {w:+.6f}")

    print("\nTraining accuracy:",
          round(100*accuracy(weights,data),2))
    print("Saved evaluator_3x3.json")

if __name__ == "__main__":
    main()
