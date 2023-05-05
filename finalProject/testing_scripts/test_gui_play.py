import logging
import os
import random
import time

import coloredlogs
import sys

from pygame.constants import *
import pygame
from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.gui import *  # Contains gui elements
from finalProject.Arena import Arena
from finalProject.utils import *

def TwoPlayers():
    pygame.init()
    import numpy



if __name__ == "__main__":

    p1_win = 0
    p2_win = 0

    board = Board(6)
    newStr = str(board)
    print(str(board))

    display_surface = init_board()

    # To accommodate AI's usage of turn (1 is P1 : -1 is P2)
    player_turn = random.randint(1, 2)
    player_turn = -1 if player_turn == 2 else 1

    game_over = False
    first_turn = True
    first_round = True
    save_first_p = 100
    highlighted_moves = set()
    selected_pit = -1

    while True:
        highlighted_moves, temp_select = draw_board(display_surface, board, player_turn, highlighted_moves, selected_pit)
        pg.display.update()

        if temp_select != -1:
            selected_pit = temp_select
        print(f"Highlighted moved: {highlighted_moves}")

        # time.sleep(0.04)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == ord("r"):

                    board = Board()
                    display_surface = init_board()

                    player_turn = random.randint(0, 1)

                    highlighted_moves, selected_pit = draw_board(display_surface, board, player_turn, highlighted_moves)
                    pg.display.update()

                    game_over = False
                    first_turn = True
                    first_round = True
                    save_first_p = 100

                    break

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = pg.mouse.get_pos()
                    print(position)

            if event.type == pg.KEYDOWN and not game_over:
                if event.key == ord("a"):

                    player_turn = (player_turn + 1) % 1

                    if first_turn:
                        save_first_p = player_turn
                        first_turn = False


                    if game_over:
                        if player_turn == 0:
                            p1_win += 1
                        if player_turn == 1:
                            p2_win += 1
                        print(f'Player 1 wins: {p1_win}')
                        print(f'Player 2 wins: {p2_win}')
                        print('[]-------------------[]')
