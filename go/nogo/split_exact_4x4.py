import csv
import random
from pathlib import Path
from collections import defaultdict

root = Path("go/nogo")
n = 4

def transform(bits, symmetry):
    result = 0
    for i in range(n*n):
        if bits & (1 << i):
            r,c = divmod(i,n)
            if symmetry >= 4:
                c = n-1-c
            for _ in range(symmetry % 4):
                r,c = c,n-1-r
            result |= 1 << (r*n+c)
    return result

def canonical(row):
    b = int(row["black_bits"])
    w = int(row["white_bits"])
    t = int(row["turn"])
    return min(
        (transform(b,s),transform(w,s),t)
        for s in range(8)
    )

with (root/"exact_4x4_sample.csv").open() as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(list)
for row in rows:
    groups[canonical(row)].append(row)

keys = sorted(groups)
random.Random(20261126).shuffle(keys)

cut = int(0.8*len(keys))
train_keys = set(keys[:cut])
test_keys = set(keys[cut:])

train = [r for r in rows if canonical(r) in train_keys]
test = [r for r in rows if canonical(r) in test_keys]

assert not train_keys & test_keys
assert len(train)+len(test)==len(rows)
assert not (
    {canonical(r) for r in train}
    & {canonical(r) for r in test}
)

for name,data in (("train",train),("test",test)):
    path = root/f"exact_4x4_{name}.csv"
    with path.open("w") as f:
        writer = csv.DictWriter(
            f,fieldnames=list(rows[0])
        )
        writer.writeheader()
        writer.writerows(data)

    wins = sum(int(r["winning"]) for r in data)
    print(name.upper())
    print("  Positions:",len(data))
    print("  Wins:",wins)
    print("  Losses:",len(data)-wins)
    print("  Win fraction:",round(wins/len(data),4))

print("Total symmetry groups:",len(groups))
print("Training groups:",len(train_keys))
print("Testing groups:",len(test_keys))
print("Symmetry leakage: NONE")
print("ALL SPLIT CHECKS PASSED")
