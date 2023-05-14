import logging
import random
import tqdm as tqdm  # Shows progress bars for loops
from gui import *

log = logging.getLogger(__name__)

class Arena:

    def __init__(self, player1, player2, game, display=None):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False):
        if (self.display):
            print(f"Current game:\n{self.game}")
        players = [self.player1, self.player2]
        cur_player = -1 if random.randint(1, 2) == 1 else 1
        board = self.game.getInitBoard()
        display_surface = init_board()
        itNum = 0
        while self.game.getGameEnded(board, cur_player) == 0:
            pg.display.update()
            player_index = 0 if cur_player == 1 else 1
            itNum += 1
            is_mcts_player = players[player_index].__name__ != 'play'
            valids = self.game.getValidMoves(board, cur_player)
            if verbose:  # Verbose represents debugging
                assert self.display
                player_turn = str(1) if cur_player == 1 else str(2)
                player_type = players[player_index].__qualname__
                player_type = player_type[0 : (len(player_type) - 5)] if not is_mcts_player else 'MCTSPlayer'
                print(f"Turn {str(itNum)} Player {player_turn} ({player_type}) ")
                self.display(display_surface, str(board), self.game.getCanonicalForm(board))
                p_pieces = board.pieces[1 if cur_player == 1 else 0]
                if player_type == "HumanPlayer":
                    for i in range(0, len(valids)):  # iterate over moves
                        if valids[i]:
                            print(f"P{1 if cur_player == 1 else 2} piece[{i}] at {p_pieces[i]}:{valids[i]}")
                action = players[player_index](display_surface, board, cur_player)
            if action[1] not in valids[action[0]]:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0

            if verbose:
                assert self.display
                print(f"Moving {str(action[0])} to index {action[1]}")

            board, cur_player = self.game.getNextState(board, cur_player, action)

        if verbose:
            assert self.display
            pg.display.update()
            self.display(display_surface, str(board), self.game.getCanonicalForm(board))
            print(f"Game over: Turn {str(itNum)}\nResult {str(self.game.getGameEnded(board, 1))}")

        return cur_player * self.game.getGameEnded(board, cur_player)

    def playGames(self, num, verbose=False):
        num = int(num / 2)
        oneWon = 0
        twoWon = 0

        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1

        return oneWon, twoWon