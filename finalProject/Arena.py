import logging
import random

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
        itNum = 0
        while self.game.getGameEnded(board, cur_player) == 0:
            player_index = 0 if cur_player == 1 else 1
            itNum += 1
            valids = self.game.getValidMoves(board, cur_player)
            player_turn = str(1) if cur_player == 1 else str(2)
            player_type = players[player_index].__qualname__
            player_type = player_type[0: (len(player_type) - 5)]
            if verbose:  # Verbose represents debugging
                assert self.display
                print(f"Turn {str(itNum)} Player {player_turn} ({player_type}) ")
                self.display(str(board))
                p_pieces = board.pieces[1 if cur_player == 1 else 0]
                if player_type == "HumanPlayer":
                    for i in range(0, len(valids)):  # iterate over moves
                        if valids[i]:
                            print(f"P{1 if cur_player == 1 else 2} piece[{i}] at {p_pieces[i]}:{valids[i]}")
            if 'MCTSPlayer' not in player_type:
                action = players[player_index](board, cur_player)
            else:
                action = players[player_index](players[1-player_index], board, cur_player)

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
            self.display(str(board))
            if cur_player == -1:
                if self.game.getGameEnded(board, cur_player) == 1:
                    wonPlayer = " Player 2 win!"
                else:
                    wonPlayer = " Player 1 win!"
            else:
                if self.game.getGameEnded(board, cur_player) == 1:
                    wonPlayer = " Player 1 win!"
                else:
                    wonPlayer = " Player 2 win!"

            print(f"Game over: Turn {str(itNum)}\nResult {wonPlayer}")
        return cur_player * self.game.getGameEnded(board, cur_player)

    def playGames(self, num, verbose=False):
        num = int(num / 2)
        oneWon = 0
        twoWon = 0

        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                print("Player 1 won!")
                oneWon += 1
            elif gameResult == -1:
                print("Player 2 won!")
                twoWon += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                print("Player 1 won!")
                oneWon += 1
            elif gameResult == 1:
                print("Player 2 won!")
                twoWon += 1

        return oneWon, twoWon