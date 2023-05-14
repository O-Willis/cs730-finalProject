import logging

# import coloredlogs

from finalProject.chinesecheckers.CCheckersLogic import Board

board = Board(6)
newStr = str(board)
print(str(board))
print()

board.execute_move(1, 1, 8)
board.execute_move(2, 2, 28)
board.execute_move(1, 1, 13)
board.execute_move(2, 3, 23)
board.execute_move(1, 5, 9)
board.execute_move(2, 0, 32)
board.execute_move(1, 0, 14)  # p1 turn should end after this
board.execute_move(2, 3, 17)
board.execute_move(1, 3, 7)
board.execute_move(2, 0, 11)
board.execute_move(2, 5, 26)  # Legal jump move
board.execute_move(1, 4, 5)
board.execute_move(2, 4, 32)
board.execute_move(1, 4, 4)
board.execute_move(2, 5, 22)
board.execute_move(1, 1, 19)
board.execute_move(2, 5, 0)
board.execute_move(2, 3, 1)  # Illegal! multi piece movement
board.execute_move(2, 4, 23)
board.execute_move(1, 3, 8)
board.execute_move(2, 0, 7)
board.execute_move(1, 3, 12)
board.execute_move(2, 2, 8)
board.execute_move(2, 1, 32)
board.execute_move(1, 2, 5)
board.execute_move(2, 0, 2)
board.execute_move(1, 4, 25)  # Turn should switch here!
board.execute_move(2, 1, 28)
board.execute_move(2, 1, 17)
board.execute_move(1, 2, 4)
board.execute_move(1, 2, 7)
board.execute_move(2, 4, 4)
board.execute_move(2, 2, 5)
board.execute_move(2, 1, 6)
print()
print(str(board))




