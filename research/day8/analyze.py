import csv, math
from pathlib import Path
root = Path(__file__).parent
rows = list(csv.DictReader((root / "exploratory_dataset.csv").open()))
data = []
for row in rows:
    name = row["ludii_title"]
    path = root / (name + "_baseline.txt")
    if not path.exists():
        path = root / (name.lower() + "_baseline.txt")
    if not path.exists():
        raise SystemExit("Missing results: " + str(path))
    values = dict(part.split("=", 1) for line in path.read_text().splitlines() for part in line.split() if "=" in part)
    if int(values["capped"]) != 0:
        raise SystemExit("Capped trials: " + name)
    data.append({"game": name, "rating": float(row["rating"]), "branching": float(values["mean_legal_moves"]), "length": float(values["mean_moves"]), "balance": float(values["Balance"])})
def pearson(x, y):
    mx, my = sum(x)/len(x), sum(y)/len(y)
    numerator = sum((a-mx)*(b-my) for a,b in zip(x,y))
    denominator = math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return numerator/denominator if denominator else float("nan")
with (root / "features_and_ratings.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["game", "rating", "branching", "length", "balance"])
    writer.writeheader()
    writer.writerows(data)
lines = ["Day 8 exploratory correlations (n=" + str(len(data)) + ")"]
for feature in ("branching", "length", "balance"):
    r = pearson([d[feature] for d in data], [d["rating"] for d in data])
    lines.append(feature + ": Pearson r = " + format(r, ".4f"))
lines.append("Exploratory only: five provisional Level B matches, random-play features, historical aggregate ratings.")
report = "\n".join(lines) + "\n"
(root / "correlations.txt").write_text(report)
print(report)
