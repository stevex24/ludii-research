import csv
import json
import time
from pathlib import Path
from features import extract, from_bits, legal_moves

root = Path("go/nogo")
weights = json.loads(
    (root/"evaluator_3x3.json").read_text()
)["weights"]

rows = list(csv.DictReader(
    (root/"exact_3x3_test.csv").open()
))

positions = [
    (int(r["black_bits"]),
     int(r["white_bits"]),
     int(r["turn"]))
    for r in rows
]

def learned(b,w,t):
    x = (1.0,) + extract(b,w,t,3)
    return sum(a*v for a,v in zip(weights,x))

def mobility(b,w,t):
    board = from_bits(b,w,3)
    return (
        len(legal_moves(board,t+1,3))
        - len(legal_moves(board,2-t,3))
    ) / 9

for name, evaluator in (
    ("Mobility", mobility),
    ("Learned", learned)
):
    start = time.perf_counter()
    checksum = 0.0

    for _ in range(10):
        for position in positions:
            checksum += evaluator(*position)

    elapsed = time.perf_counter()-start
    count = 10*len(positions)

    print(name)
    print("Evaluations:", count)
    print("Seconds:", round(elapsed,4))
    print("Evaluations/sec:", round(count/elapsed))
    print("Microseconds/evaluation:",
          round(1e6*elapsed/count,2))
    print("Checksum:", round(checksum,4))
    print()
