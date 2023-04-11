import logging
import random
import coloredlogs
import sys

from chinesecheckers.CCheckersLogic import Board
from board import *
from Arena import Arena
from utils import *

if __name__ == "__main__":
    board = Board()
    newStr = str(board)
    print(str(board))

    display_surface = init_board()

    player_turn = random.randint(1, 6)

    game_over = False
    first_turn = True
    first_round = True
    save_first_p = 100

    while True:
        draw_board(board, display_surface)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()



