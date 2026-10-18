"""KRK win/draw/loss and distance-to-mate retrograde solver.

Conventions: legal python-chess KRK positions; no 50-move/repetition rule;
rook capture leads to drawn K vs K. Distance is measured in plies.
"""
import argparse
import chess
from collections import Counter
from heapq import heappop, heappush

UNKNOWN, WIN, LOSS, DRAW = 0, 1, 2, 3

def encode(wk, wr, bk, turn):
    return (((wk * 64 + wr) * 64 + bk) * 2 + int(turn))

def decode(key):
    turn = bool(key % 2)
    key //= 2
    bk = key % 64
    key //= 64
    wr = key % 64
    wk = key // 64
    return wk, wr, bk, turn

def make_board(key):
    wk, wr, bk, turn = decode(key)
    b = chess.Board(None)
    b.set_piece_at(wk, chess.Piece(chess.KING, chess.WHITE))
    b.set_piece_at(wr, chess.Piece(chess.ROOK, chess.WHITE))
    b.set_piece_at(bk, chess.Piece(chess.KING, chess.BLACK))
    b.turn = turn
    return b

def successors(board):
    """Return (move_uci, successor_key_or_None). None means K vs K draw."""
    out = []
    for move in board.legal_moves:
        if board.is_capture(move):
            # Only possible capture in KRK is Black taking White's rook.
            out.append((move.uci(), None))
            continue
        b = board.copy(stack=False)
        b.push(move)
        wk = b.king(chess.WHITE)
        bk = b.king(chess.BLACK)
        rook = b.pieces(chess.ROOK, chess.WHITE)
        assert wk is not None and bk is not None and len(rook) == 1
        out.append((move.uci(), encode(wk, next(iter(rook)), bk, b.turn)))
    return out

def enumerate_states():
    states = []
    for wk in chess.SQUARES:
        for wr in chess.SQUARES:
            if wk == wr:
                continue
            for bk in chess.SQUARES:
                if bk == wk or bk == wr:
                    continue
                for turn in (chess.WHITE, chess.BLACK):
                    k = encode(wk, wr, bk, turn)
                    if make_board(k).is_valid():
                        states.append(k)
    return states

def sample():
    print('KRK move-generator checks')
    for fen in ('8/8/8/8/8/R7/8/k1K5 b - - 0 1',
                '8/8/8/8/8/8/1r6/K1k5 w - - 0 1',
                '8/8/8/8/8/8/1R6/K1k5 b - - 0 1'):
        b = chess.Board(fen)
        print('FEN:', fen, 'valid:', b.is_valid(),
              'mate:', b.is_checkmate(), 'stalemate:', b.is_stalemate())
        if b.is_valid() and b.pieces(chess.ROOK, chess.WHITE):
            print('Moves:', successors(b))
    print('PASS: sample enumeration completed')

def solve():
    print('Enumerating legal states...', flush=True)
    keys = enumerate_states()
    index = {k:i for i,k in enumerate(keys)}
    n = len(keys)
    print('Legal KRK states:', n, flush=True)
    assert n == 399112, f'Unexpected count {n}'
    # Compact predecessor linked lists: one node per directed non-capture edge.
    from array import array
    head = array('i', [-1]) * n
    pred = array('i')
    link = array('i')
    remaining = array('i', [0]) * n
    max_child_dtm = array('i', [0]) * n
    outcome = bytearray(n)
    dtm = array('i', [-1]) * n
    heap = []
    counters = Counter()
    print('Generating legal moves and predecessor graph...', flush=True)
    for i,k in enumerate(keys):
        b = make_board(k)
        if b.is_checkmate():
            outcome[i] = LOSS
            dtm[i] = 0
            heappush(heap, (0, i))
            counters['checkmate'] += 1
            continue
        if b.is_stalemate():
            outcome[i] = DRAW
            counters['stalemate'] += 1
            continue
        moves = successors(b)
        remaining[i] = len(moves)
        for _, target in moves:
            if target is None:
                # A rook capture is a draw, so this state cannot be a forced loss.
                counters['rook_capture_draw_edges'] += 1
                continue
            j = index.get(target)
            if j is None:
                raise RuntimeError('Legal successor missing from state set')
            pred.append(i)
            link.append(head[j])
            head[j] = len(pred)-1
        counters['edges'] += len(moves)
    print('Propagating optimal results...', flush=True)
    while heap:
        d, child = heappop(heap)
        if d != dtm[child]:
            continue
        edge = head[child]
        while edge != -1:
            parent = pred[edge]
            if outcome[parent] == UNKNOWN:
                if outcome[child] == LOSS:
                    # First discovered losing child has minimum DTM (min-heap).
                    outcome[parent] = WIN
                    dtm[parent] = d+1
                    heappush(heap, (d+1, parent))
                elif outcome[child] == WIN:
                    remaining[parent] -= 1
                    if d > max_child_dtm[parent]:
                        max_child_dtm[parent] = d
                    if remaining[parent] == 0:
                        outcome[parent] = LOSS
                        dtm[parent] = max_child_dtm[parent]+1
                        heappush(heap, (dtm[parent], parent))
            edge = link[edge]
    counts = Counter(outcome)
    max_dtm = max((dtm[i] for i in range(n) if outcome[i] in (WIN,LOSS)), default=0)
    print('RESULTS (side to move):')
    print('Winning:', counts[WIN])
    print('Losing:', counts[LOSS])
    print('Drawn:', counts[DRAW]+counts[UNKNOWN], '(including unresolved cycles)')
    print('Max DTM in plies:', max_dtm)
    print('Checkmates:', counters['checkmate'], 'Stalemates:', counters['stalemate'])
    print('Rook-capture-to-draw edges:', counters['rook_capture_draw_edges'])
    print('Directed legal moves:', counters['edges'])
    assert sum(counts.values()) == n
    assert counters['checkmate'] == 216
    assert counters['stalemate'] == 68
    with open('reports/day02_results.txt','w') as f:
        f.write('KRK retrograde analysis; no 50-move or repetition rules\n')
        f.write(f'Legal states: {n}\nWinning: {counts[WIN]}\nLosing: {counts[LOSS]}\n')
        f.write(f'Drawn: {counts[DRAW]+counts[UNKNOWN]}\nMax DTM plies: {max_dtm}\n')
        f.write(f'Checkmates: {counters["checkmate"]}\nStalemates: {counters["stalemate"]}\n')
    print('Saved reports/day02_results.txt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', action='store_true', help='Quick successor check')
    parser.add_argument('--solve', action='store_true', help='Full KRK tablebase')
    args = parser.parse_args()
    if args.solve:
        solve()
    else:
        sample()
