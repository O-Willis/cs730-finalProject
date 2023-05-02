from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.chinesecheckers.CCheckersPlayers import HumanPlayer
from finalProject.chinesecheckers.CCheckersGame import CCheckersGame as Game


game = Game(6)
humanPlayer = HumanPlayer(game).play

display_surface = Game.display

player = 1
board = game.getInitBoard()
game.display(str(board))
temp = game.getCanonicalForm(board, player)
action = humanPlayer(display_surface, temp, player)
board, _ = game.getNextState(board, player, action)
game.display(str(board))
temp = game.getCanonicalForm(board, player)
action = humanPlayer(display_surface, temp, player)
board, _ = game.getNextState(board, player, action)
game.display(str(board))