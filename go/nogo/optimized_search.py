import json
import time
from pathlib import Path
from functools import lru_cache
from fast_features import analyze
from fast_features import fast_extract,fast_extract_D
from features import from_bits

ROOT = Path(__file__).resolve().parent

MODELS = {
    "learned_3x3": "evaluator_3x3.json",
    "learned_4x4_A": "evaluator_4x4_A.json",
    "learned_4x4_D": "evaluator_4x4_D.json"
}

WEIGHTS = {
    name: json.loads(
        (ROOT/file).read_text()
    )["weights"]
    for name,file in MODELS.items()
}

class Timeout(Exception):
    pass

def child(b,w,t,m):
    if t == 0:
        return b|(1<<m),w,1
    return b,w|(1<<m),0

def optimized_search(
    b,w,t,n,seconds,
    evaluator="learned_3x3",
    use_tt=True
):
    start = time.perf_counter()
    deadline = start+seconds

    nodes = 0
    hits = 0
    cutoffs = 0
    table = {}

    @lru_cache(maxsize=100000)
    def move_sets(b,w):
        moves,_ = analyze(from_bits(b,w,n),n)
        return (
            tuple(sorted(moves[1])),
            tuple(sorted(moves[2]))
        )

    def moves(b,w,t):
        return move_sets(b,w)[t]

    @lru_cache(maxsize=100000)
    def evaluate(b,w,t):
        if evaluator == "mobility":
            return (
                len(moves(b,w,t))
                -len(moves(b,w,1-t))
            )/(n*n)

        if evaluator == "learned_4x4_D":
            x = fast_extract_D(b,w,t,n)
        else:
            x = fast_extract(b,w,t,n)

        return sum(
            a*v for a,v in
            zip(WEIGHTS[evaluator],(1.0,)+x)
        )

    def check_time():
        if time.perf_counter() >= deadline:
            raise Timeout

    def search(b,w,t,d,alpha,beta):
        nonlocal nodes,hits,cutoffs

        nodes += 1
        check_time()

        key = (b,w,t)
        entry = table.get(key) if use_tt else None
        preferred = None

        if entry is not None:
            hits += 1
            ed,ev,flag,preferred = entry

            if ed == d:
                if flag == "EXACT":
                    return ev
                if flag == "LOWER" and ev >= beta:
                    return ev
                if flag == "UPPER" and ev <= alpha:
                    return ev

        alpha0,beta0 = alpha,beta

        options = moves(b,w,t)

        if not options:
            return -1000.0

        if d == 0:
            value = evaluate(b,w,t)
            check_time()
            return value

        if preferred in options:
            options = (preferred,)+tuple(
                m for m in options if m != preferred
            )

        best = -float("inf")
        best_move = options[0]

        for m in options:
            value = -search(
                *child(b,w,t,m),
                d-1,-beta,-alpha
            )

            if value > best:
                best = value
                best_move = m

            alpha = max(alpha,value)

            if alpha >= beta:
                cutoffs += 1
                break

        if use_tt:
            if best <= alpha0:
                flag = "UPPER"
            elif best >= beta0:
                flag = "LOWER"
            else:
                flag = "EXACT"

            if entry is None or d >= entry[0]:
                if len(table)<200000 or key in table:
                    table[key] = (
                        d,best,flag,best_move
                    )

        return best

    options = moves(b,w,t)

    if not options:
        return {
            "move":None,"depth":0,
            "score":-1000.0,"nodes":0,
            "tt_hits":0,"tt_entries":0,
            "cutoffs":0,"proven":True,
            "elapsed":time.perf_counter()-start
        }

    best_move = options[0]
    best_score = None
    completed = 0

    remaining = n*n-bin(b|w).count("1")

    for depth in range(1,remaining+1):
        try:
            ordered = [best_move]+[
                m for m in options
                if m != best_move
            ]

            score = -float("inf")
            selected = best_move

            for m in ordered:
                check_time()

                value = -search(
                    *child(b,w,t,m),
                    depth-1,-float("inf"),-score
                )

                if value > score:
                    score = value
                    selected = m

            check_time()

            best_move = selected
            best_score = score
            completed = depth

            if abs(score)>=1000:
                break

        except Timeout:
            break

    return {
        "move":best_move,
        "depth":completed,
        "score":best_score,
        "nodes":nodes,
        "tt_hits":hits,
        "tt_entries":len(table),
        "cutoffs":cutoffs,
        "elapsed":time.perf_counter()-start,
        "proven":(
            best_score is not None
            and abs(best_score)>=1000
        )
    }

if __name__ == "__main__":
    for n in (3,4,5,7,9):
        result = optimized_search(0,0,0,n,1.0)
        print(f"{n}x{n}: {result}")
