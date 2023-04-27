import math

import pygame as pg
import sys

BACKGROUND = (142, 210, 255)  # Dull Blue

# EMPTY_CELL = (213, 192, 155)  # White? Or maybe orange
# EMPTY_CELL = (127, 127, 127)  # Grey
EMPTY_CELL = (92, 62, 41)  # Grey/brown

PLAYER1_RED = (255, 0, 0)
PLAYER1_RED_DEST = (255, 100, 100)

PLAYER2_GREEN = (0, 200, 0)
PLAYER2_GREEN_DEST = (100, 200, 100)

#HIGHLIGHT = (0, 255, 255)
HIGHLIGHT = (212, 212, 70)

CIRCLE_RADIUS = 20

# board constants
H_MARGIN_DISTANCE = 20
V_MARGIN_DISTANCE = 20
CIRCLE_DIAMETER = 2 * CIRCLE_RADIUS
H_SPACING = 8
V_SPACING = 1
WINDOW_WIDTH = (H_MARGIN_DISTANCE * 2) + (CIRCLE_DIAMETER * 13)
WINDOW_HEIGHT = (V_MARGIN_DISTANCE * 2) + (CIRCLE_DIAMETER * 17)
START_Y_COORD = 3.8*(V_MARGIN_DISTANCE + CIRCLE_RADIUS)

#GAME_BOARD = (185, 142, 77)
# GAME_BOARD = (122, 71, 40)
GAME_BOARD = (150, 93, 53)
GAME_BOARD_UNDER = (56, 28, 16)
GAME_BOARD_RADIUS = WINDOW_WIDTH/2.2

def init_board():
    pg.init()
    display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Chinese Checkers')
    return display_surface

def draw_board(display, board, player_turn, highlighted, selected_pit):
    display.fill(BACKGROUND)
    pg.draw.circle(display, GAME_BOARD_UNDER, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (GAME_BOARD_RADIUS + 5), 0)
    pg.draw.circle(display, GAME_BOARD, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), GAME_BOARD_RADIUS, 0)
    display_title(display)
    display_player_turn_text(display, player_turn)

    # Indicates what pit index is a new row
    newLines = [0, 2, 5, 9, 14, 20, 25, 29, 32, 34, 35]

    # Sets the y_coordinate to around the center of window
    y_coord = START_Y_COORD

    highlighted_moves = highlighted

    # sets initial x_coord to center
    x_coord = WINDOW_WIDTH/2

    ######  NOTE: FOR AI WE NEED TO ADJUST GUI FOR PLAYER TURN
    player_turn = 0 if player_turn == 1 else 1
    pieceIndexes = board.pieces[player_turn]  # To get the board indexes of a player's pieces

    rowCounter = 0
    for pit in range(0, 36):
        for i in range(0, len(pieceIndexes)):
            if pit == pieceIndexes[i]:
                # print(f"Found player {player_turn} piece {i} at index {pit}")
                break
        if pit in newLines:
            color_circle(board, pit, display, highlighted_moves, x_coord, y_coord)
            rowCounter += 1
            y_coord += CIRCLE_DIAMETER + V_SPACING
            if rowCounter < 6:
                x_coord -= rowCounter * (CIRCLE_DIAMETER + H_SPACING) - 25
            else:
                x_coord = (WINDOW_WIDTH/11+2) + (-rowCounter*25) + rowCounter * (CIRCLE_DIAMETER + H_SPACING)
        else:
            color_circle(board, pit, display, highlighted_moves, x_coord, y_coord)
            x_coord += CIRCLE_DIAMETER + H_SPACING

    # Check if the left mouse button is clicked
    if pg.mouse.get_pressed()[0]:
        highlighted_moves, selected_pit = highlight_selected_moves(board, display, player_turn, selected_pit, highlighted_moves, pieceIndexes)

    return highlighted_moves, selected_pit

def display_title(display_surface):
    font = pg.font.SysFont(None, 50)
    title_text = font.render('Chinese Checkers!', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 50))
    display_surface.blit(title_text, title_rect)

def display_player_turn_text(display_surface, player_turn):
    font = pg.font.SysFont(None, 30)
    player = 1 if player_turn == 1 else 2  # Determines indexer based on player num (1 == P1 and -1 == P2)
    title_text = font.render(f'Player {player} turn', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-80))
    display_surface.blit(title_text, title_rect)

def highlight_selected_moves(board, display_surface, pturn, selected_pit, highlighted_moves, pieces):
    # Get the mouse position
    mouse_pos = pg.mouse.get_pos()
    # Gets possible moves for given player's turn (0 if 1, 1 if 2)
    possibleMoves = board.get_legal_moves(pturn)
    # Check if the mouse is within range of any circle
    for pit in range(0, 36):
        x_coord, y_coord = get_circle_coords(pit)
        sqx = (x_coord - mouse_pos[0])**2
        sqy = (y_coord - mouse_pos[1])**2

        if (math.sqrt(sqx + sqy)) < CIRCLE_RADIUS**2:
            # print(f"Circle {pit} clicked!")
            player_piece = -1
            for i in range(0, len(pieces)):
                if pit == pieces[i]:
                    player_piece = i
                    # print(f"Found player {player_turn} piece {i} at index {pit}")
                    break
            if player_piece == -1:
                color_new_circle(board, pit, display_surface, pturn, highlighted_moves, x_coord, y_coord)
            if player_piece != -1:  # if clicked pit is a player piece
                if selected_pit != pit:  # If the pit is not the same as the previously selected
                    for highlighted in highlighted_moves:  # Highlight new moves
                        x_coord, y_coord = get_circle_coords(highlighted)
                        color_circle(board, pit, display_surface, highlighted_moves, x_coord, y_coord)
                else:
                    selected_pit = pit
                    highlighted_moves = set(possibleMoves[player_piece])  # TODO NEED TO TEST GUI ON HIGHLIGHTED MOVES!!
                    highlight_potential_moves(highlighted_moves, player_piece, display_surface)

    return highlighted_moves, selected_pit

# Not entirely sure how this method is being used
# NOTE: DOES NOT INTERFERE WITH EMPTY CELL COLORING
def color_destination(board, display_surface, x_coord, y_coord, pit):
    if pit in board.pieces[0]:  # If the pit matches the player 1's piece index
        pg.draw.circle(display_surface, PLAYER1_RED_DEST, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    if pit in board.pieces[1]:  # If the pit matches the player 2's piece index
        pg.draw.circle(display_surface, PLAYER2_GREEN_DEST, (x_coord, y_coord), CIRCLE_RADIUS, 0)

def color_new_circle(board, board_value, display_surface, player_turn, highlighted_moves, x_coord, y_coord):
    # print(f"New piece index for {player_turn} {board.pieces[player_turn]}")
    if board_value in board.pieces[0]:
        pg.draw.circle(display_surface, PLAYER1_RED, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    elif board_value in board.pieces[1]:
        pg.draw.circle(display_surface, PLAYER2_GREEN, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    else:
        pg.draw.circle(display_surface, HIGHLIGHT if board_value in list(highlighted_moves) else EMPTY_CELL,
                       (x_coord, y_coord), CIRCLE_RADIUS, 0)

def color_circle(board, board_value,display_surface, highlighted_moves, x_coord, y_coord):
    # print(f"Current coordinates for {board_value}: [{x_coord}, {y_coord}]")
    if board_value in board.pieces[0]:
        pg.draw.circle(display_surface, PLAYER1_RED, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    elif board_value in board.pieces[1]:
        pg.draw.circle(display_surface, PLAYER2_GREEN, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    else:
        pg.draw.circle(display_surface, HIGHLIGHT if board_value in list(highlighted_moves) else EMPTY_CELL,
                       (x_coord, y_coord), CIRCLE_RADIUS, 0)

def get_circle_coords(pit):
    y_coord = START_Y_COORD
    newLines = [0, 2, 5, 9, 14, 20, 25, 29, 32, 34, 35]
    x_coord_short = WINDOW_WIDTH/2
    rowCounter = 0
    for i in range(0, pit):
        if i in newLines:
            rowCounter += 1
            y_coord += CIRCLE_DIAMETER + V_SPACING
            if rowCounter < 6:
                x_coord_short -= rowCounter * (CIRCLE_DIAMETER + H_SPACING) - 25
            else:
                x_coord_short = (WINDOW_WIDTH/11+2) + (-rowCounter*25) + rowCounter * (CIRCLE_DIAMETER + H_SPACING)
        else:
            x_coord_short += CIRCLE_DIAMETER + H_SPACING
    x_coord = x_coord_short + ((pit in [28, 35]) * (CIRCLE_RADIUS + 4))
    return x_coord, y_coord

def highlight_potential_moves(highlighted_moves, selected_piece, display_surface):
    # print(f"Highlighting for selected_piece: {selected_piece}")
    for pit in highlighted_moves:
        x_coord, y_coord = get_circle_coords(pit)
        pg.draw.circle(display_surface, HIGHLIGHT, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    return highlighted_moves  # This allows highlighted moves values to stay persistent


# def highlight_best_move(best_move, display_surface):
#
#     [start_x, start_y] = best_move[0]
#     [end_x, end_y] = best_move[1]
#
#     circle_start_x, circle_start_y = find_circle_from(start_x, start_y)
#     pg.draw.ellipse(display_surface, HIGHLIGHT, (circle_start_x - CIRCLE_RADIUS, circle_start_y - CIRCLE_RADIUS,
#                                                  CIRCLE_DIAMETER, CIRCLE_DIAMETER), 5)
#
#     circle_end_x, circle_end_y = find_circle_from(end_x, end_y)
#     pg.draw.ellipse(display_surface, HIGHLIGHT, (circle_end_x - CIRCLE_RADIUS, circle_end_y - CIRCLE_RADIUS,
#                                                  CIRCLE_DIAMETER, CIRCLE_DIAMETER), 5)
#
# def find_circle_from(x, y):
#
#     if x % 2 == 0:
#         circle_x = int(H_MARGIN_DISTANCE + CIRCLE_RADIUS + (CIRCLE_DIAMETER + H_SPACING) * (y / 2))
#     else:
#         circle_x = int(H_MARGIN_DISTANCE + CIRCLE_DIAMETER + (H_SPACING / 2) + (CIRCLE_DIAMETER + H_SPACING) * ((y - 1)
#                                                                                                                 / 2))
#     circle_y = V_MARGIN_DISTANCE + CIRCLE_RADIUS + (CIRCLE_DIAMETER + V_SPACING) * x
#
#     return circle_x, circle_y

# def color_destination(board, display_surface, x_coord_long, y_coord, row, circle_in_a_row):
#     if [row, circle_in_a_row * 2] == board.pieces[4]:
#         pg.draw.circle(display_surface, PLAYER1_RED, (x_coord_long, y_coord), CIRCLE_RADIUS, 0)
#     if [row, circle_in_a_row * 2] == destinations[5]:
#         pg.draw.circle(display_surface, PLAYER2_GREEN, (x_coord_long, y_coord), CIRCLE_RADIUS, 0)



