import json
from pathlib import Path
from train_evaluator import load_data, score

root = Path("go/nogo")
model = json.loads(
    (root / "evaluator_3x3.json").read_text()
)
weights = model["weights"]

train = load_data("exact_3x3_train.csv")
test = load_data("exact_3x3_test.csv")

majority = int(
    sum(y for x,y in train)*2 >= len(train)
)

def mobility(x):
    return x[1]-x[2]

def exclusive(x):
    return x[3]-x[4]

methods = {
    "Majority class": lambda x: majority,
    "Relative mobility": lambda x: int(
        mobility(x) >= -1e-12
    ),
    "Exclusive mobility": lambda x: int(
        exclusive(x) >= -1e-12
    ),
    "Learned evaluator": lambda x: int(
        score(weights,x) >= 0
    ),
}

print("Held-out positions:", len(test))
print("Actual wins:", sum(y for x,y in test))
print("Actual losses:", sum(1-y for x,y in test))

for name, predict in methods.items():
    correct = sum(predict(x)==y for x,y in test)
    print(
        f"{name:22s}: "
        f"{correct}/{len(test)} "
        f"({100*correct/len(test):.2f}%)"
    )

tp = tn = fp = fn = 0

for x,y in test:
    p = methods["Learned evaluator"](x)
    if p and y:
        tp += 1
    elif not p and not y:
        tn += 1
    elif p and not y:
        fp += 1
    else:
        fn += 1

print("\nLearned evaluator confusion matrix:")
print("Correct win predictions:", tp)
print("Correct loss predictions:", tn)
print("Incorrect win predictions:", fp)
print("Incorrect loss predictions:", fn)
