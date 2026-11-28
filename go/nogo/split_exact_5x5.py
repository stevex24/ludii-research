import csv
import random
from pathlib import Path
from collections import defaultdict
from fast_features import analyze
from features import from_bits

root = Path("go/nogo")
N = 5
rng = random.Random(20261127)

with (root/"exact_5x5_sample.csv").open() as f:
    rows = list(csv.DictReader(f))

def transform(bits,rotation,reflection):
    result = 0

    for i in range(N*N):
        if not bits & (1<<i):
            continue

        r,c = divmod(i,N)

        if reflection:
            c = N-1-c

        for _ in range(rotation):
            r,c = c,N-1-r

        result |= 1<<(r*N+c)

    return result

def canonical(b,w,t):
    return min(
        (
            transform(b,k,f),
            transform(w,k,f),
            t
        )
        for k in range(4)
        for f in (False,True)
    )

groups = defaultdict(list)
seen = set()

for row in rows:
    b,w,t = (
        int(row[k])
        for k in ("black_bits","white_bits","turn")
    )

    assert (b,w,t) not in seen
    seen.add((b,w,t))

    assert not b&w
    assert bin(b|w).count("1")==int(row["ply"])

    legal = set(map(
        int,row["legal_move_list"].split()
    ))

    winning = set(map(
        int,row["winning_move_list"].split()
    ))

    actual,_ = analyze(from_bits(b,w,N),N)

    assert legal == actual[t+1]
    assert winning <= legal
    assert len(legal)==int(row["legal_moves"])
    assert len(winning)==int(row["winning_move_count"])
    assert bool(winning)==bool(int(row["winning"]))

    groups[canonical(b,w,t)].append(row)

keys = sorted(groups)
rng.shuffle(keys)

cut = int(0.8*len(keys))
train_keys = keys[:cut]
test_keys = keys[cut:]

assert not set(train_keys)&set(test_keys)

train = [
    row for key in train_keys
    for row in groups[key]
]

test = [
    row for key in test_keys
    for row in groups[key]
]

assert len(train)+len(test)==len(rows)

def save(name,data):
    with (root/name).open("w") as f:
        writer = csv.DictWriter(
            f,fieldnames=list(rows[0])
        )
        writer.writeheader()
        writer.writerows(data)

def report(name,data):
    wins = sum(int(r["winning"]) for r in data)

    mixed = sum(
        0<int(r["winning_move_count"])
        <int(r["legal_moves"])
        for r in data
    )

    pairs = sum(
        int(r["winning_move_count"]) *
        (int(r["legal_moves"])-
         int(r["winning_move_count"]))
        for r in data
    )

    print("\n"+name)
    print("Positions:",len(data))
    print("Winning:",wins)
    print("Losing:",len(data)-wins)
    print("Mixed positions:",mixed)
    print("Good/bad move pairs:",pairs)

save("exact_5x5_train.csv",train)
save("exact_5x5_test.csv",test)

print("Total symmetry groups:",len(keys))
print("Training groups:",len(train_keys))
print("Test groups:",len(test_keys))

report("TRAINING SET",train)
report("TEST SET",test)

print("\nALL SPLIT AND CONSISTENCY CHECKS PASSED")
