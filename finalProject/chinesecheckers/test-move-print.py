from CCheckersLogic import Board

board = Board()
newStr = str(board)
print(str(board))

print(board.get_legal_moves(1))
board.execute_move(1, 2, 7)
print(str(board))
print(board.get_legal_moves(1))