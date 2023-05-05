import unittest
import numpy as np
from finalProject.Game import Game
from finalProject.chinesecheckers.CCheckersLogic import Board
from finalProject.chinesecheckers.CCheckersGame import CCheckersGame as Game

class TestGame(unittest.TestCase):

    # def setUp(self):
        # self.n = 6
        # self.board = getInitBoard()

    def test_get_game_ended(self):
        game = Game(6)
        board = game.getInitBoard()
        b = np.copy(board.pieces)

        player = -1  # -1 for player 2
        canonical = game.getCanonicalForm(board, player)

        self.assertEqual(game.getGameEnded(canonical, player), 0)

    def test_get_next_state(self):
        game = Game(6)
        board = game.getInitBoard()
        player = -1  # -1 for player 2
        s = game.stringRepresentation(board)

        next_board, next_player = Game.getNextState(board, self.player, self.action)
        # TODO: Add assertions to check that the returned next_board and next_player are as expected
        # self.assertEqual(rectangle.get_area(), 6, "incorrect area")

if __name__ == '__main__':
    unittest.main()