import numpy as np
from finalProject.gui import *
from finalProject.chinesecheckers.CCheckersNode import Node
import pygame as pg
import sys
import time

class HumanPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valid = self.game.getValidMoves(board, player)  # Get valid moves as list
        # pieces = self.game.getNumpyFromCannonical(board)
        highlighted_moves = set()
        selected_pit = -1
        entered_input = False
        while True:  # While loop for input
            a = input()

            piece, user_move = [int(x) for x in a.split(' ')]
            piece = int(piece)
            if piece != -1:  # -1 will be the optional termination command
                user_move = int(user_move)
                if user_move in valid[piece]:
                    break
                else:
                    print("Incorrect input!!")
            else:
                break

            # highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            # pg.display.update()
            # if temp_select != -1:
            #     selected_pit = temp_select
            # user_move = -1
            # for event in pg.event.get():
            #
            #     if event.type == pg.MOUSEBUTTONDOWN:
            #         position = pg.mouse.get_pos()
            #         highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            #         pg.display.update()
            #         # piece, user_move = [int(x) for x in a.split(' ')]
            #         piece = int(piece)
            #         if piece != -1:  # -1 will be the optional termination command
            #             user_move = int(user_move)
            #             if user_move in valid[piece]:
            #                 break
            #             else:
            #                 print("Incorrect input!!")
            #             # if piece < 0 or piece > 6:
            #
            #             # if isMovingPiece(event.pos):
            #
            #
            #             # while userMove not in board.get_legal_moves(player_turn)[piece]:
            #             #     print(f"current move: {piece} to {userMove}")
            #             #     piece, userMove = input("That is not a valid piece move! Please retry!: ").split()
            #             #     piece = int(piece)
            #             #     userMove = int(userMove)
            #             #
            #             # if board.execute_move(player_turn, piece, userMove) == True:
            #             #     player_turn = (player_turn % 2) + 1
            #
            #         else:
            #             entered_input = True
            #             break

            if entered_input is True:
                break

        return [piece, user_move]


class RandPlayer:

    def __init__(self, game):
        self.game = game
        self.threshold = 10

    def play(self, display_surface, board, player):
        player_index = 1 if player == 1 else 0
        p_pieces = board.pieces[player_index]
        valid = self.game.getValidMoves(board, player)
        piece = self.get_valid_piece(valid)  # ensure that the valid array is not empty at index 'piece'
        move_index = np.random.randint(len(valid[piece]))
        while not self.is_better_move(player, board, p_pieces[piece], valid[piece][move_index]):
            piece = self.get_valid_piece(valid)
            move_index = np.random.randint(len(valid[piece]))
        # time.sleep(0.5)
        return [piece, valid[piece][move_index]]

    def get_valid_piece(self, valid):
        cur_piece = np.random.randint(self.game.getActionSize())
        while len(valid[cur_piece]) == 0:
            cur_piece = np.random.randint(self.game.getActionSize())
        return cur_piece

    def is_better_move(self, player, board, current_piece_index, valid_move_index):
        if player == 1:
            cur_piece_score = board.scorePlayer1[current_piece_index][0]
            valid_move_score = board.scorePlayer1[valid_move_index][0]
        else:
            cur_piece_score = board.scorePlayer2[current_piece_index][0]
            valid_move_score = board.scorePlayer2[valid_move_index][0]
        return valid_move_score >= cur_piece_score

class MinMaxPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE


class MCTSPlayer:

    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.root = None

        # self.Qsa = {}  # stores Q values for s,a
        # self.Nsa = {}  # contains the num of times edge s,a was visited
        # self.Ns = {}  # contains num times board s was visited
        # self.Ps = {}  # stores policy
        #
        # self.Es = {}  # contains the bool for if a game has ended for board s
        # self.Vs = {}  # contains the valid moves for board s

    def play(self, display_surface, state, player):
        if self.root is None or state != self.root.state:
            self.root = Node(self.game, state, player)
            self.root.visits += 1

        opposing_player = RandPlayer(self.game).play

        for i in range(self.args.numMCTSSims):  # Iteration for loop
            self.root = self.root.selection(opposing_player)

        return self.root.best_child().action

