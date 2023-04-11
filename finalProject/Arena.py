import logging

import tqdm as tqdm  # Shows progress bars for loops
from board import *

log = logging.getLogger(__name__)  # TODO need to implement custom __name__ for game

class Arena():

    def __init__(self, player1, player2, game, display=None):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display
        self.display_surface = init_board()

    def playGame(self, verbose=False):  # TODO Need to understand how turn taking & action taking works!!!
        if (self.display):
            print(f"Current game:\n{self.game}")
        players = [self.player1, None, self.player2]
        curPlayer = 1  # Player 1 will always go first
        board = self.game.getInitBoard()
        itNum = 0
        while self.game.getGameEnded(board, curPlayer) == 0:
            itNum += 1
            if verbose:  # Verbose represents debugging
                assert self.display
                print("Turn", str(itNum), "Player ", str(curPlayer))
                self.display(board)
            action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))

            valids = self.game.getValidMoves(self.game.getCanonicalForm(board, curPlayer), 1)

            if valids[action] == 0:  # TODO recheck the logic here. POSSIBLE FOR 0
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            if verbose:
                assert self.display
                print(f"Game over: Turn {str(itNum)}\nResult {str(self.game.getGameEnded(board, 1))}")
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    def playGames(self, num, verbose=False):
        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0  # TODO THIS IS POSSIBLE, CHECK LOGIC

        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws