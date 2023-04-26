import logging

import coloredlogs

from CCheckersLogic import Board
#from ..Arena import Arena
#from ..utils import *

# Issue sequence:
# p2 first  :: 1 28 - invalid
    # 1 27
# p1        :: 1  7 - invalid
    # 1 8
# p2        :: 5 23
# p1        :: 5 12
# p2        :: 3 29
# p1        :: 1 13

# testing for multi-jump::
# p2        :: 2 28 -> :: 2 17 -> :: 2 8 -> :: 2 1 -> :: -1 -1
# p1
#

board = Board()
newStr = str(board)
print(str(board))
print()

board.execute_move(2, 1, 27)
print(str(board))
board.execute_move(1, 1, 8)
print(str(board))
board.execute_move(2, 5, 23)
print(str(board))
print(board.get_legal_moves(1))
board.execute_move(1, 5, 12)


# board2 = Board()
# newStr2 = str(board2)
# print(str(board2))
# print()
#
# print(board2.get_legal_moves(1))
# board2.execute_move(1, 2, 7)
# print(str(board2))
# print(board2.get_legal_moves(1))
# if (board2.is_game__over(1)):
#     print("Your winner!")



