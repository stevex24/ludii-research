from functools import lru_cache

FEATURE_NAMES = (
    "own_mobility",
    "opponent_mobility",
    "own_exclusive",
    "opponent_exclusive",
    "shared_moves",
    "empty_fraction",
    "stone_advantage",
    "liberty_advantage",
    "constrained_advantage",
)

@lru_cache(None)
def neighbors(n):
    result = []
    for i in range(n*n):
        r, c = divmod(i, n)
        result.append(tuple(
            rr*n+cc
            for rr, cc in (
                (r-1,c), (r+1,c),
                (r,c-1), (r,c+1)
            )
            if 0 <= rr < n and 0 <= cc < n
        ))
    return tuple(result)

def groups(board, color, n):
    seen = set()
    adj = neighbors(n)
    result = []

    for i in range(n*n):
        if board[i] != color or i in seen:
            continue

        stack = [i]
        seen.add(i)
        stones = set()
        liberties = set()

        while stack:
            j = stack.pop()
            stones.add(j)

            for k in adj[j]:
                if board[k] == 0:
                    liberties.add(k)
                elif board[k] == color and k not in seen:
                    seen.add(k)
                    stack.append(k)

        result.append((stones, liberties))

    return result

def legal_moves(board, color, n):
    moves = set()

    for i, value in enumerate(board):
        if value != 0:
            continue

        trial = list(board)
        trial[i] = color

        if all(
            liberties
            for c in (1, 2)
            for stones, liberties in groups(trial, c, n)
        ):
            moves.add(i)

    return moves

def from_bits(black, white, n):
    return [
        1 if black & (1 << i)
        else 2 if white & (1 << i)
        else 0
        for i in range(n*n)
    ]

def extract(black, white, turn, n):
    board = from_bits(black, white, n)
    own = turn + 1
    opp = 3 - own
    area = n*n

    a = legal_moves(board, own, n)
    b = legal_moves(board, opp, n)

    ga = groups(board, own, n)
    gb = groups(board, opp, n)

    def avg_lib(g):
        return sum(len(l) for s,l in g)/max(1,len(g))

    def constrained(g):
        return sum(len(l)==1 for s,l in g)

    return (
        len(a)/area,
        len(b)/area,
        len(a-b)/area,
        len(b-a)/area,
        len(a&b)/area,
        board.count(0)/area,
        (board.count(own)-board.count(opp))/area,
        (avg_lib(ga)-avg_lib(gb))/area,
        (constrained(gb)-constrained(ga))/area,
    )

if __name__ == "__main__":
    for n in (3, 5, 7):
        print(f"\nEmpty {n}x{n} board:")
        for name, value in zip(
            FEATURE_NAMES, extract(0,0,0,n)
        ):
            print(f"{name}: {value:.4f}")
