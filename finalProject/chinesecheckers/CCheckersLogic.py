'''
Class for Board
Data:
    1=White, -1=Black, 0=Empty
    Dimensions are as follows:
        column x row
Pits are stored and manipulated as (x,y) tuples
x is the column, y is the row.
'''

'''
Things needed to keep track off:
    - Getting all legal moves of a specific piece and color/player
    - Executing that move
    - Indicating when a turn is over
        * Undoing a move (or not lol)
    - 

'''

class Board():
    # directions as (x,y) offsets
    __directions = [()]

    def __init__(self, n):
        """Initial configuration of the board"""

        self.n = n
        # Initialize empty board
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # TODO set up initial pieces on both sides of board
        # ex:
        #   self.pieces[int(self.n/2)-1][int(self.n/2)] = 1
        #   self.pieces[int(self.n/2)-1][int(self.n/2)-1] = -1

    def __getitem__(self, index):
        return self.pieces[index]

    def countDiff(self, color):  # TODO need reimplementation based on logic of game
        """
        Intended to count # pieces of given color
        (1 for white, -1 for black, 0 for empty spaces)
        """
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    count += 1
                if self[x][y] == -color:
                    count -= 1
        return count

    def get_legal_moves(self, color):
        """Returns all legal moves for given color/player
        (1 for white, -1 for black)
        """
        moves = set()  # storage of legal moves

        # Get all pits with pieces of given color
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    newMoves = self.get_moves_for_position((x,y))
                    moves.update(newMoves)
        return list(moves)

    def has_legal_moves(self, color):
        """
        TODO might need to reimplement as goal state
            ie. when player has crossed all pieces
            |
            Might not need to in edge case for if other player traps a piece
        """

        """
        Receive all legal moves given a color
        """
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == color:
                    newMoves = self.get_moves_for_position((x,y))
                    if len(newMoves) > 0:
                        return True
        return False

    def get_moves_for_position(self, pit):
        """
        Returns all legal moves that use the given square
        """
        (x,y) = pit

        # Find color of piece
        color = self[x][y]

        # skip over empty squares
        if color == 0:
            return None

        moves = []
        for direction in self.__directions:
            move = self.__discover_move(pit, direction)
            if move:
                # print(square, move, direction)
                moves.append(move)

        return moves

    def execute_move(self, move, color):  # TODO
        """
        Performs the given move on the board.
        """

