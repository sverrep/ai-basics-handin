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
    xcount = 0
    ocount = 0
    for row in board:
        for value in row:
            if value == X:
                xcount += 1
            elif value == O:
                ocount += 1
    
    if xcount == 0 and ocount == 0:
        return X
    elif xcount > ocount:
        return O
    elif xcount == ocount:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)
    if action not in possible_actions:
        print(action)
        raise Exception("Action is not possible")
    current_player = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    row = find_row_winner(board)
    if row:
        return row

    col = find_col_winner(board)
    if col:
        return col
    
    diag = find_diag_winner(board)
    if diag:
        return diag
    
    return None
    
def find_row_winner(board):
    for row in board:
        xrow = 0
        orow = 0
        for value in row:
            if value == X:
                xrow += 1
            elif value == O:
                orow += 1
        if xrow == 3:
            return X
        elif orow == 3:
            return O

def find_col_winner(board):
    for i in range(3):
        xcol = 0
        ocol = 0
        for j in range(3):
            if board[j][i] == X:
                xcol += 1
            elif board[j][i] == O:
                ocol += 1
        if xcol == 3:
            return X
        elif ocol == 3:
            return O

def find_diag_winner(board):
    xdiag = 0
    odiag = 0
    xdiag2 = 0
    odiag2 = 0
    j = 2
    for i in range(3):
        if board[i][i] == X:
            xdiag += 1
        if board[i][i] == O:
            odiag += 1
        if board[i][j] == X:
            xdiag2 += 1
        if board[i][j] == O:
            odiag2 += 1
        j -= 1

    if xdiag == 3 or xdiag2 == 3:
        return X
    if odiag == 3 or odiag2 == 3:
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    
    if winner(board) is not None:
        return True

    for x in range(3):
        for y in range(3):
            if board[x][y] == EMPTY:
                return False
    return True
    



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    global all_actions
    all_actions = 0

    if terminal(board):
      return None

    if player(board) == 'X':
      best_move = maxValue(board)
      print("Actions explored", all_actions)
      print(best_move)
      return best_move[0]
    else:
      best_move = minValue(board)
      print("Actions explored", all_actions)
      print(best_move)
      return best_move[0]
    
    

def maxValue(board, min = 5):
    global all_actions
    
    if terminal(board):
        return (None, utility(board))
    
    option = -5
    best_action = None
    for action in actions(board):
        if min <= option:
            break
        all_actions += 1

        potential_option = minValue(result(board, action), option)

        if potential_option[1] > option:
            option = potential_option[1]
            best_action = action

    return (best_action, option)


def minValue(board, max = -5):
    global all_actions

    if terminal(board):
        return (None, utility(board))

    option = 5
    best_action = None
    for action in actions(board):
        if max >= option:
            break

        all_actions += 1

        potential_option = maxValue(result(board, action), option)

        if potential_option[1] < option:
            option = potential_option[1]
            best_action = action

    return (best_action, option)