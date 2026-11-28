import json
import optimized_search as engine
from pathlib import Path

root = Path(__file__).resolve().parent

models = {
    "learned_5x5_A":"evaluator_5x5_A.json",
    "learned_5x5_D":"evaluator_5x5_D.json",
    "ranking_5x5":"evaluator_5x5_ranking.json"
}

for name,filename in models.items():
    model = json.loads(
        (root/filename).read_text()
    )

    weights = model["weights"]
    indices = model["feature_indices"]

    full = [weights[0]]+[0.0]*9

    for i,value in zip(indices,weights[1:]):
        full[i+1] = value

    engine.WEIGHTS[name] = full

optimized_search = engine.optimized_search

if __name__ == "__main__":
    for name in models:
        result = optimized_search(
            0,0,0,5,0.1,name,True
        )

        print(name,result)

    print("ALL NEW MODELS REGISTERED")
