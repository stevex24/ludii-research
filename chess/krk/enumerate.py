import chess
from collections import Counter

def krk_board(wk, wr, bk, turn):
    board = chess.Board(None)
    board.set_piece_at(wk, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(wr, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(bk, chess.Piece(chess.KING, chess.BLACK))
    board.turn = turn
    return board

def main():
    counts = Counter()
    example_mate = None
    for wk in chess.SQUARES:
        for wr in chess.SQUARES:
            if wr == wk:
                continue
            for bk in chess.SQUARES:
                if bk == wk or bk == wr:
                    continue
                for turn in (chess.WHITE, chess.BLACK):
                    counts['placements'] += 1
                    board = krk_board(wk, wr, bk, turn)
                    if not board.is_valid():
                        continue
                    counts['legal'] += 1
                    if board.is_checkmate():
                        counts['checkmate'] += 1
                        if example_mate is None:
                            example_mate = board.fen()
                    elif board.is_stalemate():
                        counts['stalemate'] += 1
    print(dict(counts))
    print('Example checkmate:', example_mate)

if __name__ == '__main__':
    main()
