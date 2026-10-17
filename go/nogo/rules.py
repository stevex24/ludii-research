"""NoGo move legality on an n x n grid. 0 empty, 1 black, 2 white."""

def neighbors(i, n):
    r, c = divmod(i, n)
    if r > 0: yield i - n
    if r + 1 < n: yield i + n
    if c > 0: yield i - 1
    if c + 1 < n: yield i + 1


def valid_board(board):
    n = __import__('math').isqrt(len(board))
    if n < 1 or n * n != len(board) or any(x not in (0, 1, 2) for x in board):
        raise ValueError('board must be a nonempty square tuple/list with values 0,1,2')
    return n


def groups_have_liberties(board):
    n = valid_board(board)
    seen = set()
    for start, color in enumerate(board):
        if color == 0 or start in seen:
            continue
        stack = [start]
        seen.add(start)
        liberty = False
        while stack:
            pos = stack.pop()
            for j in neighbors(pos, n):
                if board[j] == 0:
                    liberty = True
                elif board[j] == color and j not in seen:
                    seen.add(j)
                    stack.append(j)
        if not liberty:
            return False
    return True


def legal_moves(board, player):
    """Indices where player may place a stone without capture or suicide."""
    valid_board(board)
    if player not in (1, 2):
        raise ValueError('player must be 1 or 2')
    if not groups_have_liberties(board):
        raise ValueError('input board has a group without liberties')
    result = []
    for i, value in enumerate(board):
        if value != 0:
            continue
        after = list(board)
        after[i] = player
        if groups_have_liberties(after):
            result.append(i)
    return result


def play(board, player, index):
    if index not in legal_moves(board, player):
        raise ValueError('illegal NoGo move')
    after = list(board)
    after[index] = player
    return tuple(after)
