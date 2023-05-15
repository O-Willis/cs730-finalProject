import numpy as np

moves = [
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
jumpMoves = [
    [3, 5],                     # edge 0
    [6, 8],                     # edge 1
    [7, 9],                     # edge 2
    [0, 10, 12, 5],             # edge 3
    [11, 13],                   # mid 4
    [0, 3, 12, 14],             # edge 5
    [1, 8, 15, 17],             # edge 6
    [2, 9, 16, 18],             # mid 7
    [1, 6, 17, 19],             # mid 8
    [2, 7, 18, 20],             # edge 9
    [3, 12, 22],                # edge 10
    [4, 13, 21, 23],            # mid 11
    [3, 5, 10, 14, 22, 24],     # mid 12
    [4, 11, 23, 25],            # mid 13
    [5, 12, 24],                # edge 14
    [6, 17, 26],                # edge 15
    [7, 18, 27],                # mid 16
    [6, 8, 15, 19, 26, 28],     # mid 17
    [7, 9, 16, 20, 27, 29],     # mid 18
    [8, 17, 28],                # mid 19
    [9, 18, 29],                # edge 20
    [11, 23, 30],               # edge 21
    [10, 12, 24, 31],           # mid 22
    [11, 13, 21, 25, 30, 32],   # mid 23
    [12, 14, 22, 31],           # mid 24
    [13, 23, 32],               # edge 25
    [15, 17, 28, 33],           # edge 26
    [16, 18, 29, 34],           # mid 27
    [17, 19, 26, 33],           # mid 28
    [18, 20, 27, 34],           # edge 29
    [21, 23, 32, 35],           # edge 30
    [22, 24],                   # mid 31
    [23, 25, 30, 35],           # edge 32
    [26, 28],                   # edge 33
    [27, 29],                   # edge 34
    [30, 32]                    # edge 35
]

# distance calculations for player 1
scorePlayer2 = [
              [-16],                    # row 1
           [-12],[-12],                 # row 2
         [-9], [-9], [-9],              # row 3
      [-7], [-7], [-7], [-7],           # row 4
   [-6], [-6], [-6], [-6], [-6],        # row 5
[-5], [-5], [-5], [-5], [-5], [-5],     # row 6
   [-4], [-4], [-4], [-4], [-4],        # row 7
      [-3], [-3], [-3], [-3],           # row 8
         [-2], [-2], [-2],              # row 9
            [-1], [-1],                 # row 11
                [0]]                    # row 12

# distance calculations for player 2
scorePlayer1 = [
                 [0],                   # row 1
             [-1], [-1],                # row 2
          [-2], [-2], [-2],             # row 3
       [-3], [-3], [-3], [-3],          # row 4
    [-4], [-4], [-4], [-4], [-4],       # row 5
 [-5], [-5], [-5], [-5], [-5], [-5],    # row 6
    [-6], [-6], [-6], [-6], [-6],       # row 7
       [-7], [-7], [-7], [-7],          # row 8
          [-9], [-9], [-9],             # row 9
            [-12], [-12],               # row 11
               [-16]]                   # row 12

moves_array = [np.array(x) for x in moves]  # makes a numpy of all individual moves
jump_moves_array = [np.array(x) for x in jumpMoves]  # makes a numpy of all individual moves
goal = [None] * 6
for i in range(6):
    goal[i] = [0] * 6
goal = np.zeros((2,6), dtype=int)
goal[0, :] = 35 - np.array([5, 4, 3, 2, 1, 0])  # player 1s goal
goal[1, :] = np.array([5, 4, 3, 2, 1, 0])


class Board:

    def __init__(self, n):
        """Initial configuration of the board"""

        self.n = n  # Number of pieces
        self.pieces = np.zeros((2, 6), dtype=int)
        #  [0,:] splices array and all column values become assigned
        self.pieces[0, :] = [0, 1, 2, 3, 4, 5]
        self.pieces[1, :] = 35 - np.array([5, 4, 3, 2, 1, 0])

    def duplicate(self):
        board_copy = Board(6)
        board_copy.pieces = np.copy(self.pieces)
        return board_copy

    @property
    def pieces(self):
        return self._pieces

    @pieces.setter
    def pieces(self, value):
        self._pieces = value

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
                    tmpP2 = index == self.pieces[0,:]
                    tmpP1 = index == self.pieces[1,:]
                    arr1 = np.array([0, 1, 2, 3, 4, 5])
                    if np.sum(tmpP1):
                        out += f" 1_{arr1[tmpP1].item()}  "
                    elif np.sum(tmpP2):
                        out += f" 2_{arr1[tmpP2].item()}  "
                    else:
                        out += "  -   "
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
        board_map = np.zeros((36))
        board_map[self.pieces] = 1  # Assigns 1 to both Player1 and Player2
        # Indicates if the spot is occupied

        # Get all pits with pieces of given color
        playerInd = 1 if player == 1 else 0
        for pit in range(self.n):
            closed_list = set()
            validMoves = self.determine_jumps(closed_list, board_map, pit, playerInd, True)
            out.append(list(set(validMoves)))
        return out

    def determine_jumps(self, closed_list, board_map, pit, player_index, is_first):
        # given pit, get index
        piece_index = self.pieces[player_index, pit]  # :, specifies 1st column
        closed_list.add(piece_index)
        single_moves = moves_array[piece_index]  # Formats into an array for the actual moves
        # This filters out all moves that aren't possible given position
        valid_single_moves = single_moves[board_map[single_moves] == 0]  # 0 represents empty pit for move to be made
        valid_moves = list(valid_single_moves) if is_first else []
        jump_moves = jump_moves_array[piece_index]
        single_invalid_moves = single_moves[board_map[single_moves] != 0]  # represents invalid moves
        valid_jump_moves = []
        # If there is an intersection between a single's valid move
        for invalidMove in list(single_invalid_moves):
            potentialJumpMoves = moves_array[invalidMove]
            # Find if there is space for a potential jump move
            validPotentialJumpMoves = potentialJumpMoves[board_map[potentialJumpMoves] == 0]
            for i in range(jump_moves.shape[0]):  # going over the valid moves
                if sum(jump_moves[i] == validPotentialJumpMoves):
                    valid_jump_moves.append(jump_moves[i])
                    break

        valid_moves.extend(valid_jump_moves)  # Grows the list
        for move in valid_jump_moves:
            if move in closed_list: continue
            temp = self.pieces[player_index, pit]
            self.pieces[player_index, pit] = move
            valid_moves.extend(self.determine_jumps(closed_list, board_map, pit, player_index, False))
            self.pieces[player_index, pit] = temp
        return valid_moves

    def has_legal_moves(self, player):
        """
        Receive all legal moves given a color
        """
        cur_moves = self.get_legal_moves(player)
        return len(cur_moves) == 0

    def get_valid_single_moves(self, board_map, piece):
        """
        Gives all single moves given the player and piece number
        """
        single_moves = moves_array[piece]
        valid_single_moves = single_moves[board_map[single_moves] == 0]
        return valid_single_moves

    def get_valid_jump_moves(self, board_map, piece):
        jump_moves = jump_moves_array[piece]
        single_moves = moves_array[piece]
        single_invalid_moves = single_moves[board_map[single_moves] != 0]  # represents invalid moves
        validJumpMoves = []
        # If there is an intersection between a single's valid move
        for invalidMove in list(single_invalid_moves):
            potentialJumpMoves = moves_array[invalidMove]
            # Find if there is space for a potential jump move
            validPotentialJumpMoves = potentialJumpMoves[board_map[potentialJumpMoves] == 0]
            for i in range(jump_moves.shape[0]):  # going over the valid moves
                if sum(jump_moves[i] == validPotentialJumpMoves):
                    validJumpMoves.append(jump_moves[i])
                    break
        return validJumpMoves

    def is_valid_piece_move(self, player, piece, action):
        """
        Performs a check on an action to verify that the action is a valid action
        """
        board_map = np.zeros((36))
        board_map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        p_index = 1 if player == 1 else 0  # Determines indexer based on player num (1 == P1 and -1 == P2)
        piece_index = self.pieces[p_index, piece]  # gets the pieceIndex for given piece of player
        valid_single_moves = self.get_valid_single_moves(board_map, piece_index)
        valid_jump_moves = self.get_valid_jump_moves(board_map, piece_index)
        action_is_single = action in valid_single_moves
        action_is_jump = action in valid_jump_moves
        if action_is_single is True and action_is_jump is True:
            assert(action_is_single is not action_is_jump)

        if action in valid_single_moves:
            return True

        elif action in valid_jump_moves:
            return True
        else:
            return False



    def execute_move(self, player, player_piece, action):
        """
        Performs the given move on the board.
        In terms of cutting down on calculation size,
            the AI should point to where a piece should go,
            and the code will determine if a piece can actually go there or not
        """
        moves = self.get_legal_moves(player)
        # Should never call on execute if no moves are able to be made
        assert len(list(moves)) > 0

        board_map = np.zeros((36))
        board_map[self.pieces] = 1  # Important for defining where the players pieces are (both P1 and P2!!)
        player_index = 1 if player == 1 else 0  # Determines indexer based on player num (1 == P1 and -1 == P2)
        piece_index = self.pieces[player_index, player_piece]  # gets the pieceIndex for given piece of player

        valid_single_moves = self.get_valid_single_moves(board_map, piece_index)
        valid_jump_moves = self.get_valid_jump_moves(board_map, piece_index)
        action_is_single = action in valid_single_moves
        action_is_jump = action in valid_jump_moves
        if action_is_single is True and action_is_jump is True:
            assert(action_is_single is not action_is_jump)

        if action in moves[player_piece]:
            self.pieces[player_index, player_piece] = action

        if action_is_single:
            return True  # Return True if changePlayers
        else:
            nextJumps = self.get_valid_jump_moves(board_map, player_piece)
            if len(nextJumps) == 1 and piece_index in nextJumps:
                return True
            else:
                return False


    def is_game_over(self, player):
        player_index = 1 if player == 1 else 0  # Determines indexer based on player num (1 == P1 and -1 == P2)
        opponent_index = 0 if player_index == 1 else 1
        is_in_goal = np.sum(np.reshape(self.pieces[player_index, :], (6, 1)) == goal[player_index]) == 6
        if is_in_goal:
            return True
        player_start_index = (opponent_index) * 35  # If player 1, 35 or if player 2, 0
        opponent_in_init_corner = (self.pieces[opponent_index, :] == player_start_index).any()
        five_pieces_in_goal = np.sum(np.reshape(self.pieces[player_index, :], (6, 1)) == goal[player_index]) == 5
        is_blocked = five_pieces_in_goal and opponent_in_init_corner
        if is_blocked:
            return True
        return False
