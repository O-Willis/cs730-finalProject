class Game:
    """
    1 for player1 and -1 for player2.
    """

    def __init__(self):
        pass

    def getInitBoard(self):
        """
        Returns:
            b: a representation of the initial board
        """
        pass

    def getActionSize(self):
        """
        Returns:
            a constant number 6
        """
        pass

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by the current player
        Returns:
            (b, -player)
            b: the board after the action
            -player: the next player after the action
        """
        pass

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player
        Returns:
            legal_moves:
            a list of actions that can be made for each pits
        """
        pass

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            0 if game is not finished.
            1 if player won,
            -1 if player lost,
        """
        pass


    def getScore(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)
        Returns:
            score: the score of the game state, depending on both players location
        """
        pass

    def getStringRepresentation(self):
        """
        Returns:
            conversion of board data structure to game visualization.
        """
        pass