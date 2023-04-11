import pygame as pg


BACKGROUND = (142, 210, 255)  # Dull Blue

EMPTY_CELL = (213, 192, 155)  # White? Or maybe orange

PLAYER1_RED = (255, 0, 0)

PLAYER2_GREEN = (0, 200, 0)

HIGHLIGHT = (0, 255, 255)

CIRCLE_RADIUS = 20

# board constants
H_MARGIN_DISTANCE = 20
V_MARGIN_DISTANCE = 20
CIRCLE_DIAMETER = 2 * CIRCLE_RADIUS
H_SPACING = 8
V_SPACING = 1
WINDOW_WIDTH = (H_MARGIN_DISTANCE * 2) + (CIRCLE_DIAMETER * 13)
WINDOW_HEIGHT = (V_MARGIN_DISTANCE * 2) + (CIRCLE_DIAMETER * 17)

def init_board(self):
    pg.init()
    display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Chinese Checkers')
    return display_surface

def draw_board(board, display_surface):
    display_surface.fill(BACKGROUND)

    y_coord = V_MARGIN_DISTANCE + CIRCLE_RADIUS

    destinations = [[2, 0], [0, 8], [2, 24], [14, 24], [16, 16], [14, 0]]

    for row in range(0, 17):
        x_coord_long = H_MARGIN_DISTANCE + CIRCLE_RADIUS
        x_coord_short = int(H_MARGIN_DISTANCE + CIRCLE_DIAMETER + (H_SPACING / 2))

        for circle_in_a_row in range(0, 13):
            if row % 2 == 0:
                board_value = board[row][circle_in_a_row * 2]
                if [row, circle_in_a_row * 2] in destinations:
                    color_desination(display_surface, x_coord_long, y_coord, row, circle_in_a_row, destinations)
                else:
                    color_circle(board_value, display_surface, x_coord_long, y_coord)

                x_coord_long = x_coord_long + CIRCLE_DIAMETER + H_SPACING

                ## TODO FILL IN MORE HERE

def color_circle(board_value, display_surface, x_coord, y_coord):
    if board_value == -1:
        pg.draw.circle(display_surface, BACKGROUND, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    if board_value == 0:
        pg.draw.circle(display_surface, EMPTY_CELL, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    if board_value == 1:
        pg.draw.circle(display_surface, PLAYER1_RED, (x_coord, y_coord), CIRCLE_RADIUS, 0)
    if board_value == 2:
        pg.draw.circle(display_surface, PLAYER2_GREEN, (x_coord, y_coord), CIRCLE_RADIUS, 0)

def color_destination(display_surface, x_coord_long, y_coord, row, circle_in_a_row, destinations):
    if [row, circle_in_a_row * 2] == destinations[4]:
        pg.draw.circle(display_surface, PLAYER1_RED, (x_coord_long, y_coord), CIRCLE_RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[5]:
        pg.draw.circle(display_surface, PLAYER2_GREEN, (x_coord_long, y_coord), CIRCLE_RADIUS, 0)



