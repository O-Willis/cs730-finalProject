from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.chinesecheckers.CCheckersPlayers import HumanPlayer
from finalProject.chinesecheckers.CCheckersGame import CCheckersGame as Game
from finalProject.gui_2 import *


game = Game(6)
humanPlayer = HumanPlayer(game).play

display_surface = init_board()

player = 1
board = game.getInitBoard()
cannonical = game.getCanonicalForm(board, player)
game.display(display_surface, str(board), cannonical)
action = humanPlayer(display_surface, cannonical, player)
board, _ = game.getNextState(board, player, action)
cannonical = game.getCanonicalForm(board, player)
game.display(display_surface, str(board), cannonical)
action = humanPlayer(display_surface, cannonical, player)
board, _ = game.getNextState(board, player, action)
cannonical = game.getCanonicalForm(board, player)
game.display(display_surface, str(board), cannonical)