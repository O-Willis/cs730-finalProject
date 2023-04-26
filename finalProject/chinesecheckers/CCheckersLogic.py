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
import numpy as np

'''
             0  
           1   2  
         3   4   5  
       6   7   8   9  
    10  11  12  13  14  
  15  16  17  18  19  20  
    21  22  23  24  25  
      26  27  28  29  
        30  31  32  
          33  34  
            35
'''


class Board():
    # directions as (x,y) offsets
    directions = [()]

    def __init__(self):
        """Initial configuration of the board"""
        self.moves = [
            [1, 2],                     # edge 0
            [0, 2, 3, 4],               # edge 1
            [0, 1, 4, 5],               # edge 2
            [1, 4, 6, 7],               # edge 3
            [1, 2, 3, 5, 7, 8],         # mid 4
            [2, 4, 8, 9],               # edge 5
            [3, 7, 10, 11],             # edge 6
            [3, 4, 6, 8, 11, 12],       # mid 7
            [4, 5, 7, 9, 12, 13],       # mid 8
            [5, 8, 13, 14],             # edge 9
            [6, 11, 15, 16],            # edge 10
            [6, 7, 10, 12, 16, 17],     # mid 11
            [7, 8, 11, 13, 17, 18],     # mid 12
            [8, 9, 12, 14, 18, 19],     # mid 13
            [9, 13, 19, 20],            # edge 14
            [10, 16, 21],               # edge 15
            [10, 11, 15, 17, 21, 22],   # mid 16
            [11, 12, 16, 18, 22, 23],   # mid 17
            [12, 13, 17, 19, 23, 24],   # mid 18
            [13, 14, 18, 20, 24, 25],   # mid 19
            [14, 19, 25],               # edge 20
            [15, 16, 22, 26],           # edge 21
            [16, 17, 21, 23, 26, 27],   # mid 22
            [17, 18, 22, 24, 27, 28],   # mid 23
            [18, 19, 23, 25, 28, 29],   # mid 24
            [19, 20, 24, 28, 29],       # edge 25
            [21, 22, 27, 30],           # edge 26
            [22, 23, 26, 28, 30, 31],   # mid 27
            [23, 24, 27, 29, 31, 32],   # mid 28
            [24, 25, 28, 31, 32],       # edge 29
            [26, 27, 31, 33],           # edge 30
            [27, 28, 30, 32, 33, 34],   # mid 31
            [28, 29, 31, 34],           # edge 32
            [30, 31, 34, 35],           # edge 33
            [31, 32, 33, 35],           # edge 34
            [33, 34]                    # edge 35
        ]
        self.jumpMoves = [
            [3, 5],                 # edge 0
            [6, 8],                 # edge 1
            [7, 9],                 # edge 2
            [0, 10, 12, 5],         # edge 3
            [11, 13],               # mid 4
            [0, 3, 12, 14],         # edge 5
            [1, 8, 15, 17],         # edge 6
            [2, 9, 16, 18],         # mid 7
            [1, 6, 17, 19],         # mid 8
            [2, 7, 18, 20],         # edge 9
            [3, 12, 22],            # edge 10
            [4, 13, 21, 23],        # mid 11
            [3, 5, 10, 14, 22, 24], # mid 12
            [4, 11, 23, 25],        # mid 13
            [5, 12, 24],            # mid 14
            [6, 17, 26],               # edge 15
            [7, 18, 27],   # mid 16
            [6, 8, 15, 19, 26, 28],   # mid 17
            [7, 9, 16, 20, 27, 29],   # mid 18
            [8, 17, 28],   # mid 19
            [9, 18, 29],               # edge 20
            [11, 23, 30],           # edge 21
            [10, 12, 24, 31],   # mid 22
            [11, 13, 21, 25, 30, 32],   # mid 23
            [12, 14, 22, 31],   # mid 24
            [13, 23, 32],       # edge 25
            [15, 17, 28, 33],           # edge 26
            [16, 18, 29, 34],   # mid 27
            [17, 19, 26, 33],   # mid 28
            [18, 20, 27, 34],       # edge 29
            [21, 23, 32, 35],           # edge 30
            [22, 24],           # mid 31
            [23, 25, 30, 35],           # edge 32
            [26, 28],           # edge 33
            [27, 29],           # edge 34
            [30, 32]                    # edge 35
        ]

        self.n = 6  # Number of pieces
        # Initialize empty board
        self.pieces = [None] * self.n
        self.goal = [None] * self.n
        for i in range(self.n):
            self.pieces[i] = [0] * self.n
            self.goal[i] = [0] * self.n

        self.pieces = np.zeros((2, 6), dtype=np.int)
        self.goal = np.zeros((2,6), dtype=np.int)
        #  [0,:] splices array and all column values become assigned
        self.pieces[0, :] = [0, 1, 2, 3, 4, 5]
        self.pieces[1, :] = 35 - np.array([0, 1, 2, 3, 4, 5])
        self.goal[0, :] = 35 - np.array([0, 1, 2, 3, 4, 5])
        self.goal[1, :] = self.pieces[0, :]

    def __getitem__(self, index):
        return self.pieces[index]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        board = [["-", " ", " ", " ", " ", " "],
                 ["-", "-", " ", " ", " ", " "],
                 ["-", "-", "-", " ", " ", " "],
                 ["-", "-", "-", "-", " ", " "],
                 ["-", "-", "-", "-", "-", " "],
                 ["-", "-", "-", "-", "-", "-"],
                 ["-", "-", "-", "-", "-", " "],
                 ["-", "-", "-", "-", " ", " "],
                 ["-", "-", "-", " ", " ", " "],
                 ["-", "-", " ", " ", " ", " "],
                 ["-", " ", " ", " ", " ", " "]]
        out = ""
        index = 0
        # for r in range(0, 11):
        #     line = board[r]
        #     linetab = r - 4
        #     if (r <= 5):
        #         linetab = 6 - r
        #     for t in range(0, linetab):
        #         out += "  "
        #     for c in range(0, len(line)):
        #         isEnd = c == len(line) - 1
        #         cur = line[c]
        #         if cur != "-" and cur != " ":
        #             out += f"{cur} "
        #         elif cur == "-":
        #             tmpP1 = index == self.pieces[0,:]
        #             tmpP2 = index == self.pieces[1,:]
        #             arr1 = np.array([0, 1, 2, 3, 4, 5])
        #             if np.sum(tmpP1):
        #                 out += f" {arr1[tmpP1].item()}  "
        #             elif np.sum(tmpP2):
        #                 out += f"-{arr1[tmpP2].item()}  "
        #             else:
        #                 out += " -  "
        #             # if index > 9:
        #             #     out += str(index) + "  "
        #             # else:
        #             #     out += " " + str(index) + "  "
        #             index += 1
        #         if isEnd or cur == " ":
        #             out += "\n"
        #             break
        for r in range(0, 11):
            line = board[r]
            linetab = r - 4
            if (r <= 5):
                linetab = 6 - r
            for t in range(0, linetab):
                out += "   "
            for c in range(0, len(line)):
                isEnd = c == len(line) - 1
                cur = line[c]
                if cur == "-":
                    tmpP1 = index == self.pieces[0,:]
                    tmpP2 = index == self.pieces[1,:]
                    arr1 = np.array([0, 1, 2, 3, 4, 5])
                    if np.sum(tmpP1):
                        out += f" 1_{arr1[tmpP1].item()}  "
                    elif np.sum(tmpP2):
                        out += f" 2_{arr1[tmpP2].item()}  "
                    else:
                        out += "  -   "
                    # if index > 9:
                    #     out += str(index) + "  "
                    # else:
                    #     out += " " + str(index) + "  "
                    index += 1
                if isEnd or cur == " ":
                    out += "\n"
                    break
        return out

    def get_legal_moves(self, player):
        """Returns all legal moves for given color/player
        (1 for white, -1 for black)
        """
        out = []
        map = np.zeros((36))
        map[self.pieces] = 1  # Assigns 1 to both Player1 and Player2
        # Indicates if the spot is occupied

        # Get all pits with pieces of given color
        playerInd = 0 if player == 1 else 1
        for pit in range(self.n):
            closed_list = set()
            validMoves = self.method_name(closed_list, map, pit, playerInd, True)
            out.append(list(set(validMoves)))
        return out

    def method_name(self, closed_list, map, pit, playerInd, isFirst):
        # given pit, get index
        pieceInd = self.pieces[playerInd, pit]  # :, specifies 1st column
        closed_list.add(pieceInd)
        singleMoves = np.array(self.moves[pieceInd])  # Formats into an array for the actual moves
        # This filters out all moves that aren't possible given position
        validSingleMoves = singleMoves[map[singleMoves] == 0]  # 0 represents empty pit for move to be made
        validMoves = list(validSingleMoves) if isFirst else []
        jumpMoves = np.array(self.jumpMoves[pieceInd])
        singleInvalidMoves = singleMoves[map[singleMoves] != 0]  # represents invalid moves
        validJumpMoves = []
        # If there is an intersection between a single's valid move
        for invalidMove in list(singleInvalidMoves):
            potentialJumpMoves = np.array(self.moves[invalidMove])
            # Find if there is space for a potential jump move
            validPotentialJumpMoves = potentialJumpMoves[map[potentialJumpMoves] == 0]
            for i in range(jumpMoves.shape[0]):  # going over the valid moves
                if sum(jumpMoves[i] == validPotentialJumpMoves):
                    validJumpMoves.append(jumpMoves[i])
                    break

        validMoves.extend(validJumpMoves)  # Grows the list
        for move in validJumpMoves:
            if move in closed_list: continue
            temp = self.pieces[playerInd, pit]
            self.pieces[playerInd, pit] = move
            validMoves.extend(self.method_name(closed_list, map, pit, playerInd, False))
            self.pieces[playerInd, pit] = temp
        return validMoves

    def has_legal_moves(self, player):
        """
        TODO might need to reimplement as goal state
            ie. when player has crossed all pieces
            |
            Might not need to in edge case for if other player traps a piece
        """
        """
        Receive all legal moves given a color
        """
        curMoves = self.get_legal_moves(player)
        return len(curMoves) == 0

    def get_position_moves(self, pit):  # TODO
        """
        Returns all legal moves that use the given square
        """
        (x, y) = pit

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

    def get_valid_single_moves(self, player, piece):
        """
        Gives all single moves given the player and piece number
        """
        map = np.zeros((36))
        map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        playerInd = 0 if player == 1 else 1  # Determines indexer based on player num (1 == P1 and -1 == P2)
        pieceInd = self.pieces[playerInd, piece]  # gets the pieceIndex for given piece of player
        # print(f"Current piece's board index: {pieceInd}")
        singleMoves = np.array(self.moves[pieceInd])
        validSingleMoves = singleMoves[map[singleMoves] == 0]
        return validSingleMoves

    def get_valid_jump_moves(self, player, piece):
        map = np.zeros((36))
        map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        playerInd = 0 if player == 1 else 1  # Determines indexer based on player num (1 == P1 and -1 == P2)
        pieceInd = self.pieces[playerInd, piece]  # gets the pieceIndex for given piece of player
        jumpMoves = np.array(self.jumpMoves[pieceInd])
        singleMoves = np.array(self.moves[pieceInd])
        singleInvalidMoves = singleMoves[map[singleMoves] != 0]  # represents invalid moves
        validJumpMoves = []
        if player == 1 and piece == 5:
            x = 0
        # If there is an intersection between a single's valid move
        for invalidMove in list(singleInvalidMoves):
            potentialJumpMoves = np.array(self.moves[invalidMove])
            # Find if there is space for a potential jump move
            validPotentialJumpMoves = potentialJumpMoves[map[potentialJumpMoves] == 0]
            # print(f"Valid potential jump moves: {validPotentialJumpMoves}")
            for i in range(jumpMoves.shape[0]):  # going over the valid moves
                # print(f"cur jumpMoves: {jumpMoves[i]}")
                if sum(jumpMoves[i] == validPotentialJumpMoves):
                    validJumpMoves.append(jumpMoves[i])
                    break
        # print(f"Piece {piece} has valid jump moves: {validJumpMoves}")
        return validJumpMoves

    def is_valid_piece_move(self, player, piece, action):
        """
        Performs a check on an action to verify that the action is a valid action
        """
        map = np.zeros((36))
        map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        playerInd = 0 if player == 1 else 1  # Determines indexer based on player num (1 == P1 and -1 == P2)
        validSingleMoves = self.get_valid_single_moves(player, piece)
        validJumpMoves = self.get_valid_jump_moves(player, piece)
        actionIsSingle = action in validSingleMoves
        actionIsJump = action in validJumpMoves
        if actionIsSingle is True and actionIsJump is True:
            assert(actionIsSingle is not actionIsJump)

        if action in validSingleMoves:
            # print(f"{action} is a single move")
            return True

        elif action in validJumpMoves:
            # print(f"{action} is a jump move")
            return True
        else:
            return False



    def execute_move(self, player, piece, action):  # TODO might need to change framework to work with new parameters
        """
        Performs the given move on the board.
        In terms of cutting down on calculation size,
            the AI should point to where a piece should go,
            and the code will determine if a piece can actually go there or not
        """
        moves = self.get_legal_moves(player)
        # Should never call on execute if no moves are able to be made
        assert len(list(moves)) > 0
        # print(f"Moving piece {piece} to pit[{action}]")

        map = np.zeros((36))
        map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        playerInd = 0 if player == 1 else 1  # Determines indexer based on player num (1 == P1 and -1 == P2)
        orig_piece_index = self.pieces[playerInd, piece]  # gets the pieceIndex for given piece of player

        validSingleMoves = self.get_valid_single_moves(player, piece)
        validJumpMoves = self.get_valid_jump_moves(player, piece)
        actionIsSingle = action in validSingleMoves
        actionIsJump = action in validJumpMoves
        if actionIsSingle is True and actionIsJump is True:
            assert(actionIsSingle is not actionIsJump)

        if action in validSingleMoves:
            # print(f"{action} is a single move")
            x = 0

        if action in validJumpMoves:
            # print(f"{action} is a jump move")
            x = 0


        if action in moves[piece]:
            self.pieces[playerInd, piece] = action

        # TODO need to implement turn based rotating on single move
        #   as well as multi-move capabilities based on jump move

        if actionIsSingle:
            return True  # Return True if changePlayers
        else:
            nextJumps = self.get_valid_jump_moves(player, piece)
            if len(nextJumps) == 1 and orig_piece_index in nextJumps:
                return True
            else:
                return False


    def is_game__over(self, player):
        playerInd = 0 if player == 1 else 1  # Determines indexer based on player num (1 == P1 and -1 == P2)
        return False
        # if self.goal[playerInd, :] == self.pieces[playerInd, :]:
        #     return True
        # else:
        #     return False
