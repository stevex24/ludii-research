import csv
from pathlib import Path
from features import extract, from_bits, legal_moves
from solve_3x3 import legal_moves as exact_moves

def transform(bits, reflect=False):
    result = 0
    for i in range(9):
        if bits & (1 << i):
            r, c = divmod(i, 3)
            if reflect:
                rr, cc = r, 2-c
            else:
                rr, cc = c, 2-r
            result |= 1 << (3*rr+cc)
    return result

rows = list(csv.DictReader(
    Path("go/nogo/exact_3x3.csv").open()
))

asymmetric = 0

for row in rows:
    b = int(row["black_bits"])
    w = int(row["white_bits"])
    t = int(row["turn"])

    board = from_bits(b, w, 3)

    for color in (0, 1):
        expected = set(exact_moves(b, w, color))
        actual = legal_moves(board, color+1, 3)
        assert expected == actual, (b,w,color)

    f = extract(b,w,t,3)

    assert f == extract(
        transform(b), transform(w), t, 3
    )

    assert f == extract(
        transform(b,True), transform(w,True), t, 3
    )

    assert f == extract(w,b,1-t,3)

    if f[2] > 0 or f[3] > 0:
        asymmetric += 1

print("Positions tested:", len(rows))
print("PASS: Legal moves agree with exact solver")
print("PASS: Rotation invariance")
print("PASS: Reflection invariance")
print("PASS: Color-exchange invariance")
print("Positions with exclusive moves:", asymmetric)
print("Percentage:", round(100*asymmetric/len(rows),2))
