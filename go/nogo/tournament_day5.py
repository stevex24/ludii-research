import csv
import math
import random
import time
from pathlib import Path
from itertools import combinations
from optimized_search import optimized_search,child
from fast_features import analyze
from features import from_bits

root = Path("go/nogo")
rng = random.Random(20261126)

agents = (
    "mobility",
    "learned_3x3",
    "learned_4x4_A",
    "learned_4x4_D"
)

BUDGET = 0.1
OPENINGS = 10

def moves(b,w,t,n):
    m,_ = analyze(from_bits(b,w,n),n)
    return sorted(m[t+1])

def generate_openings(n):
    positions = set()

    while len(positions)<OPENINGS:
        b,w,t = 0,0,0

        for _ in range(4):
            options = moves(b,w,t,n)
            if not options:
                break

            b,w,t = child(
                b,w,t,rng.choice(options)
            )

        if moves(b,w,t,n):
            positions.add((b,w,t))

    return sorted(positions)

def play(position,n,black,white):
    b,w,t = position
    plies = 0
    nodes = 0

    while True:
        options = moves(b,w,t,n)

        if not options:
            winner = white if t==0 else black
            return winner,plies,nodes

        agent = black if t==0 else white

        result = optimized_search(
            b,w,t,n,BUDGET,agent,True
        )

        m = result["move"]
        assert m in options

        nodes += result["nodes"]
        b,w,t = child(b,w,t,m)
        plies += 1

def elo_difference(p):
    if p<=0 or p>=1:
        return None
    return 400*math.log10(p/(1-p))

games = []
summaries = []
start = time.perf_counter()

for n in (4,5):
    openings = generate_openings(n)
    standings = {
        a:{"wins":0,"games":0}
        for a in agents
    }

    print(f"\n{n}x{n} TOURNAMENT",flush=True)

    for a,b in combinations(agents,2):
        wins = 0
        count = 0

        for index,position in enumerate(openings):
            for black,white in ((a,b),(b,a)):
                winner,plies,nodes = play(
                    position,n,black,white
                )

                count += 1
                wins += int(winner==a)

                standings[black]["games"] += 1
                standings[white]["games"] += 1
                standings[winner]["wins"] += 1

                games.append({
                    "size":n,
                    "opening":index,
                    "black_bits":position[0],
                    "white_bits":position[1],
                    "turn":position[2],
                    "black":black,
                    "white":white,
                    "winner":winner,
                    "plies":plies,
                    "nodes":nodes,
                    "seconds_per_move":BUDGET
                })

        p = wins/count
        elo = elo_difference(p)

        elo_text = (
            "undefined" if elo is None
            else f"{elo:+.1f}"
        )

        print(
            f"{a} vs {b}: "
            f"{wins}-{count-wins} "
            f"({100*p:.1f}%) "
            f"relative Elo {elo_text}",
            flush=True
        )

        summaries.append({
            "size":n,
            "agent_a":a,
            "agent_b":b,
            "wins_a":wins,
            "wins_b":count-wins,
            "win_rate_a":p,
            "relative_elo_a":elo
        })

    print("\nSTANDINGS",flush=True)

    for a,r in sorted(
        standings.items(),
        key=lambda item:-item[1]["wins"]
    ):
        p = r["wins"]/r["games"]
        print(
            f"{a:20s} "
            f"{r['wins']:3d}/{r['games']} "
            f"({100*p:.1f}%)",
            flush=True
        )

for filename,data in (
    ("tournament_day5_games.csv",games),
    ("tournament_day5_summary.csv",summaries)
):
    with (root/filename).open("w") as f:
        writer = csv.DictWriter(
            f,fieldnames=list(data[0])
        )
        writer.writeheader()
        writer.writerows(data)

print("\nTotal games:",len(games))
print("Total seconds:",
      round(time.perf_counter()-start,3))
