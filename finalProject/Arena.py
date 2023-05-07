import logging
import random
import tqdm as tqdm  # Shows progress bars for loops
from gui import *

log = logging.getLogger(__name__)  # TODO need to implement custom __name__ for game

class Arena():

    def __init__(self, player1, player2, game, display=None):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False):  # TODO Need to understand how turn taking & action taking works!!!
        if (self.display):
            print(f"Current game:\n{self.game}")
        players = [self.player1, self.player2]
        cur_player = -1 if random.randint(1, 2) == 1 else 1
        # curPlayer = 1  # Player 1 will always go first
        board = self.game.getInitBoard()
        display_surface = init_board()
        itNum = 0
        while self.game.getGameEnded(board, cur_player) == 0:
            pg.display.update()
            itNum += 1
            if verbose:  # Verbose represents debugging
                assert self.display
                print("Turn", str(itNum), "Player ", str(1) if cur_player == 1 else str(2))
                self.display(display_surface, str(board), self.game.getCanonicalForm(board, cur_player))
            #  temp = self.game.getCanonicalForm(board, cur_player)
            player_index = 0 if cur_player == 1 else 1
            valids = self.game.getValidMoves(board, cur_player)
            if verbose:
                p_pieces = board.pieces[1 if cur_player == 1 else 0]
                for i in range(0, len(valids)):  # iterate over moves
                    if valids[i]:
                        print(f"P{1 if cur_player == 1 else 0} piece[{i}] at {p_pieces[i]}:{valids[i]}")
            action = players[player_index](display_surface, board, cur_player)
            if action[1] not in valids[action[0]]:  # TODO recheck the logic here. POSSIBLE FOR 0
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            if verbose:
                assert self.display
                print(f"Moving {str(action[0])} to index {action[1]}")
            board, cur_player = self.game.getNextState(board, cur_player, action)
        if verbose:
            assert self.display
            self.display(display_surface, str(board), self.game.getCanonicalForm(board, cur_player))
            print(f"Game over: Turn {str(itNum)}\nResult {str(self.game.getGameEnded(board, 1))}")
        # while not pg.mouse.get_pressed()[0]:
        #     x = 0
        return cur_player * self.game.getGameEnded(board, cur_player)

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