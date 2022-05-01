from tictactoe import terminal, utility

X = "X"
O = "O"
EMPTY = None
board = [[X, EMPTY, O],
        [EMPTY, O, EMPTY],
        [O, EMPTY, X]]

print(utility(board))