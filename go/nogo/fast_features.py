from features import neighbors, groups, from_bits

def analyze(board,n):
    adj = neighbors(n)
    info = {}
    group_at = {}

    for color in (1,2):
        info[color] = groups(board,color,n)

        for stones,liberties in info[color]:
            record = (color,liberties)
            for i in stones:
                group_at[i] = record

    moves = {1:set(),2:set()}

    for i,value in enumerate(board):
        if value != 0:
            continue

        adjacent = adj[i]

        for color in (1,2):
            capture = False
            survives = False

            for j in adjacent:
                if board[j] == 0:
                    survives = True
                    continue

                c,liberties = group_at[j]

                if c != color:
                    if len(liberties) == 1:
                        capture = True
                        break
                elif len(liberties) > 1:
                    survives = True

            if survives and not capture:
                moves[color].add(i)

    return moves,info

def fast_legal_moves(board,color,n):
    moves,_ = analyze(board,n)
    return moves[color]

def fast_extract(black,white,turn,n):
    board = from_bits(black,white,n)
    own = turn+1
    opp = 3-own
    area = n*n

    moves,info = analyze(board,n)

    a,b = moves[own],moves[opp]
    ga,gb = info[own],info[opp]

    def avg_lib(g):
        return sum(
            len(l) for s,l in g
        )/max(1,len(g))

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
        (constrained(gb)-constrained(ga))/area
    )

def fast_extract_D(black,white,turn,n):
    board = from_bits(black,white,n)
    own = turn+1
    opp = 3-own
    area = n*n

    moves,info = analyze(board,n)

    a,b = moves[own],moves[opp]
    ga,gb = info[own],info[opp]

    def avg_lib(g):
        return sum(
            len(l) for s,l in g
        )/max(1,len(g))

    def constrained(g):
        return sum(len(l)==1 for s,l in g)

    return (
        len(a-b)/area,
        len(b-a)/area,
        len(a&b)/area,
        (avg_lib(ga)-avg_lib(gb))/area,
        (constrained(gb)-constrained(ga))/area
    )
