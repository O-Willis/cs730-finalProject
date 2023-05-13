import logging

# import coloredlogs

from finalProject.chinesecheckers.CCheckersLogic import Board

board = Board(6)
newStr = str(board)
print(str(board))
print()

board.pieces[0, :] = [30, 31, 32, 33, 34, 29]
board.pieces[1, :] = [0, 1, 2, 3, 4, 35]
print(str(board))
result = board.is_game_over(1)
result_2 = board.is_game_over(-1)