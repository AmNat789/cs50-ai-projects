"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    plays = 0
    for r in board:
        for cell in r:
            if cell != EMPTY:
                plays += 1

    if plays % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a = []

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                a.append([i, j])

    return a


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    cell = board[i][j]
    if cell != EMPTY:
        raise Exception(f"Action {action} This is not a valid move, as it already has a value of {cell}")
    else:
        new_board = copy.deepcopy(board)
        new_board[i][j] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        # check rows
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # check cols
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

        # check diagonals
        if board[1][1] is not EMPTY:
            if (board[0][0] == board[1][1] == board[2][2]) or (board[2][0] == board[1][1] == board[0][2]):
                return board[1][1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    # Check if there are any empty cells

    for r in board:
        for cell in r:
            if cell is EMPTY:
                return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w is X:
        return 1
    elif w is O:
        return -1
    else:
        return 0


def max_value(board, last_action):
    if terminal(board):
        return [utility(board), last_action]
    v = [-math.inf, last_action]
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        new = min_value(result(board, action), action)
        if new[0] > v[0]:
            v = new
    return v


def min_value(board, last_action):
    if terminal(board):
        return [utility(board), last_action]
    v = [math.inf, last_action]
    for action in actions(board):
        # v = min(v, max_value(result(board, action)))
        new = max_value(result(board, action), action)
        if new[0] < v[0]:
            v = new
    return v

def do_minimax(board, last_action):
    p = player(board)

    if terminal(board):
        return [utility(board), last_action]

    v = [math.inf, last_action]
    if p is X:
        v[0] = -math.inf

    for action in actions(board):
        new = do_minimax(result(board, action), action)
        if p is X and new[0] > v[0]:
            v = new
        elif p is O and new[0] < v[0]:
            v = new

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return do_minimax(board, None)[1]

# TODO remove main after debugging
if __name__ == "__main__":
    board = [[O, EMPTY, O],
             [O, X, X],
             [X, EMPTY, X]]

    print(minimax(board))