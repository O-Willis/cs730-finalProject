import logging

import coloredlogs

from CCheckersLogic import Board
from ..Arena import Arena
from ..utils import *

board = Board()
newStr = str(board)
print(str(board))

print(board.get_legal_moves(1))
board.execute_move(1, 2, 7)
print(str(board))
print(board.get_legal_moves(1))
if (board.is_game__over(1)):
    print("Your winner!")



