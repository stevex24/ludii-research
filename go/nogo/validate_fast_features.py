import csv
import random
import time
from pathlib import Path
from features import extract,legal_moves,from_bits
from fast_features import (
    fast_extract,fast_extract_D,analyze
)

root = Path("go/nogo")
rng = random.Random(20261126)
start = time.perf_counter()

def validate(b,w,t,n):
    board = from_bits(b,w,n)
    moves,_ = analyze(board,n)

    for color in (1,2):
        assert moves[color] == legal_moves(
            board,color,n
        ), ("move mismatch",b,w,t,n,color)

    old = extract(b,w,t,n)
    new = fast_extract(b,w,t,n)
    reduced = fast_extract_D(b,w,t,n)

    assert old == new, (
        "feature mismatch",b,w,t,n,old,new
    )

    assert reduced == tuple(
        old[i] for i in (2,3,4,7,8)
    ), ("reduced feature mismatch",b,w,t,n)

for n,name in (
    (3,"exact_3x3.csv"),
    (4,"exact_4x4_sample.csv")
):
    count = 0
    with (root/name).open() as f:
        for r in csv.DictReader(f):
            b,w,t = (
                int(r[k]) for k in
                ("black_bits","white_bits","turn")
            )
            validate(b,w,t,n)
            count += 1

    print(f"{n}x{n}: {count} positions PASS")

for n in (5,7,9):
    count = 0

    for game in range(10):
        b,w,t = 0,0,0

        while True:
            validate(b,w,t,n)
            count += 1

            options = sorted(
                legal_moves(
                    from_bits(b,w,n),t+1,n
                )
            )

            if not options:
                break

            m = rng.choice(options)

            if t == 0:
                b |= 1<<m
            else:
                w |= 1<<m

            t = 1-t

    print(f"{n}x{n}: {count} positions PASS")

print("ALL VALIDATION CHECKS PASSED")
print("Seconds:",
      round(time.perf_counter()-start,3))
