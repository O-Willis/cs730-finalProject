import numpy as np
from finalProject.board import *
import pygame as pg
import sys
import time
from copy import deepcopy

class HumanPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        valid = self.game.getValidMoves(board, player)  # Get valid moves as list
        # pieces = self.game.getNumpyFromCannonical(board)
        for i in range(0, len(valid)):  # iterate over moves
            if valid[i]:
                print(f"{i}:{valid[i]}")
        highlighted_moves = set()
        selected_pit = -1
        entered_input = False
        while True:  # While loop for input

            a = input()

            piece, userMove = [int(x) for x in a.split(' ')]
            piece = int(piece)
            if piece != -1:  # -1 will be the optional termination command
                userMove = int(userMove)
                if userMove in valid[piece]:
                    break
                else:
                    print("Incorrect input!!")
            else:
                break

            # highlighted_moves, temp_select = draw_board(display_surface, pieces, player, highlighted_moves, selected_pit)
            # pg.display.update()
            # if temp_select != -1:
            #     selected_pit = temp_select
            #
            # for event in pg.event.get():
            #
            #     if event.type == pg.MOUSEBUTTONDOWN:
            #         position = pg.mouse.get_pos()
            #         highlighted_moves, temp_select = draw_board(display_surface, board, player, highlighted_moves, selected_pit)
            #         pg.display.update()
            #         # piece, userMove = [int(x) for x in a.split(' ')]
            #         piece = int(piece)
            #         if piece != -1:  # -1 will be the optional termination command
            #             userMove = int(userMove)
            #             if userMove in valid[piece]:
            #                 break
            #             else:
            #                 print("Incorrect input!!")
            #             # if piece < 0 or piece > 6:
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
            #
            # if entered_input is True:
            #     break

        return [piece, userMove]


class RandPlayer:

    def __init__(self, game):
        self.game = game
        self.threshold = 10

    def play(self, display_surface, board, player):
        curPlayer = 0 if player == -1 else 1
        valid = self.game.getValidMoves(board, player)
        print(f"Valid moves: {valid}")
        chanceNum = np.random.randint(100)
        pieces = np.copy(self.game.getPlayerPieces(board))
        piece = np.random.randint(self.game.getActionSize())
        while len(valid[piece]) == 0:  # ensure that the valid array is not empty at index 'piece'
            piece = np.random.randint(self.game.getActionSize())
        moveInd = np.random.randint(len(valid[piece]))
        if player == 1:
            if chanceNum <= self.threshold:
                return [piece, valid[piece][moveInd]]
            else:
                while not (valid[piece][moveInd] <= pieces[curPlayer, piece]):
                    piece = np.random.randint(self.game.getActionSize())
                    while len(valid[piece]) == 0:
                        piece = np.random.randint(self.game.getActionSize())
                    moveInd = np.random.randint(len(valid[piece]))
                    chanceNum = np.random.randint(100)
                    if chanceNum <= self.threshold:
                        return [piece, valid[piece][moveInd]]
        else:
            if chanceNum <= self.threshold:
                return [piece, valid[piece][moveInd]]
            while not (valid[piece][moveInd] >= pieces[curPlayer, piece]):
                piece = np.random.randint(self.game.getActionSize())
                while len(valid[piece]) == 0:
                    piece = np.random.randint(self.game.getActionSize())
                moveInd = np.random.randint(len(valid[piece]))
                chanceNum = np.random.randint(100)
                if chanceNum <= self.threshold:
                    return [piece, valid[piece][moveInd]]
        return [piece, valid[piece][moveInd]]

class MinMaxPlayer:
    # Player 1 is maximizing player / Player 2 is minimizing player
    def __init__(self, game):
        self.game = game

    def play(self, display_surface, board, player):
        # run minimax algorithm with searching depth 2
        # curPlayer = 0 if player == -1 else 1
        valid = self.game.getValidMoves(board, player)
        print(f"Valid moves: {valid}")

        result = self.minimax(board, player, 2, player, True)
        _, pieceToMove, nextIndex = result[0], result[1], result[2]
        # print(f"Moving piece {pieceToMove} to the new index of {nextIndex}")
        return [pieceToMove, nextIndex]

    def minimax(self, board, player, maxDepth, playerHeuristic, maxP):
        if maxDepth == 0 or self.game.getGameEnded(board, player) != 0:
            return [self.game.getScore(board, playerHeuristic), None, None]

        if maxP: # maximizing player
            bestValueMax = -9999
            piece = -1
            index = -1
            valids = self.game.getValidMoves(board, player)

            for i in range(len(valids)):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, player = self.game.getNextState(board, player, [i,valids[i][j]])
                    actionValue, _ , _ = self.minimax(board, player, maxDepth - 1, playerHeuristic, False)
                    if actionValue > bestValueMax:
                        bestValueMax = actionValue
                        index = valids[i][j]
                        piece = i
                    board = originalBoard
            return [bestValueMax, piece, index]

        else: # minimizing player
            piece = -1
            index = -1
            bestValueMin = 9999
            valids = self.game.getValidMoves(board, player)
            for i in range(len(valids)):
                for j in range(len(valids[i])):
                    originalBoard = deepcopy(board)
                    board, player = self.game.getNextState(board, player, [i, valids[i][j]])
                    actionValue, _ , _ = self.minimax(board, player, maxDepth - 1, playerHeuristic, True)
                    if actionValue < bestValueMin:
                        bestValueMin = actionValue
                        index = valids[i][j]
                        piece = i
                    board = originalBoard
            return [bestValueMin, piece, index]


class MCTSPlayer:

    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        # TODO IMPLEMENT MCTS HERE
