from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.chinesecheckers.CCheckersGame import CCheckersGame as Game

game = Game(6)
board = Board(6)
newStr = str(board)
print(str(board))
print()

board.execute_move(1, 2, 28)
board.execute_move(2, 3, 6)
board.execute_move(1, 5, 23)
board.execute_move(2, 0, 3)
board.execute_move(1, 5, 17)
board.execute_move(2, 5, 8)
board.execute_move(1, 3, 35)
board.execute_move(2, 3, 11)
board.execute_move(1, 3, 23)
board.execute_move(2, 4, 13)
board.execute_move(1, 3, 18)
board.execute_move(2, 3, 12)
#  Issue happens here where piece 0 should be able ot move to 11
print(str(board), end="")
p_pieces = board.pieces[1]
valids = game.getValidMoves(board, 1)
for i in range(0, len(valids)):  # iterate over moves
    if valids[i]:
        print(f"P1 piece[{i}] at {p_pieces[i]}:{valids[i]}")
x = 0








