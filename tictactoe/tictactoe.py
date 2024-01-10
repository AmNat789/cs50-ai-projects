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
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError


# TODO remove main after debugging
if __name__ == "__main__":
    board = [[O, EMPTY, O],
             [O, X, X],
             [X, EMPTY, X]]

    print(result(board, [1,1]))
