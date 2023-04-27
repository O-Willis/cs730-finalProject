from chinesecheckers.CCheckersLogic import Board
from pygame.constants import *
from finalProject.board import *
import pygame
import sys
import time

START_TURN = 1

if __name__ == "__main__":

    board = Board()
    newStr = str(board)
    print(str(board))
    display_surface = init_board()
    player_turn = START_TURN
    player_turn = -1 if player_turn == 2 else 1

    highlighted_moves = set()
    selected_pit = -1

    turn_num = 0

    while True:
        highlighted_moves, temp_select = draw_board(display_surface, board, player_turn, highlighted_moves, selected_pit)
        pg.display.update()
        if temp_select != -1:
            selected_pit = temp_select
        #print(f"Highlighted moved: {highlighted_moves}")

        time.sleep(0.04)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = pg.mouse.get_pos()
                    # print(position)

                    pturn = 0 if player_turn == 1 else 1
                    print(f"Previous player moves: {board.pieces[pturn]}")
                    if turn_num == 0:
                        board.execute_move(1, 1, 8)
                    elif turn_num == 1:
                        board.execute_move(2, 1, 27)
                    elif turn_num == 2:
                        board.execute_move(1, 5, 12)
                    elif turn_num == 3:
                        board.execute_move(2, 5, 23)
                    else:
                        turn_num = 0
                        board = Board()

                    print(f"Click num: {turn_num}")
                    print(f"Post player moves: {board.pieces[pturn]}")
                    turn_num += 1

                    player_turn = (player_turn % 2) + 1
                    selected_pit = -1
                    highlighted_moves = set()

                    highlighted_moves, temp_select = draw_board(display_surface, board, player_turn,
                                                                highlighted_moves, selected_pit)
                    print(f"selected pit: {selected_pit}")
                    print(f"highlighted moves: {highlighted_moves}")
                    pg.display.update()

                    if (turn_num > 3):
                        print("======================================")

                if event.type == pg.KEYDOWN:
                    if event.key == ord("r"):

                        board = Board()
                        display_surface = init_board()

                        highlighted_moves, selected_pit = draw_board(display_surface, board, player_turn, highlighted_moves)
                        pg.display.update()