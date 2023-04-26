import sys
import os
import random
import logging
import coloredlogs
from chinesecheckers.CCheckersLogic import Board
# from Arena import Arena

def printHelp():
    print("usage: run.py [-h] ... [-c cmd | -m mod | file | -] [arg] ...\n"
          "Options and arguments (and corresponding environment variables):")

    print("optional arguments:")
    print("  -h, --help\tshow this help message and exit")
    exit(0)

def printBoard(board):
    for r in range(0, len(board)):
        line = board[r]
        linetab = r-1
        if (r <= 5):
            linetab = 9 - r
        for t in range(0, linetab):
            print("  ", end="")
        for c in range(0, len(line)):
            isEnd = c == len(line)-1
            cur = line[c]
            if cur != "-" and cur != " ":
                print(f"{cur}", end=" ")
            elif cur == "-":
                print(" - ", end=" ")
            if isEnd or cur == " ":
                print()
                break

if __name__ == "__main__":
    init = [["1_1", " ", " ", " ", " ", " "],
            ["1_2", "1_3", " ", " ", " ", " "],
            ["1_4", "1_5", "1_6", " ", " ", " "],
            ["-", "-", "-", "-", " ", " "],
            ["-", "-", "-", "-", "-", " "],
            ["-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", " "],
            ["-", "-", "-", "-", " ", " "],
            ["2_4", "2_5", "2_6", " ", " ", " "],
            ["2_2", "2_3", " ", " ", " ", " "],
            ["2_1", " ", " ", " ", " ", " "]]
    print("\n")
    printBoard(init)
    print(f"Arguments count: {len(sys.argv)}")
    if '-help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
        printHelp()
    if '-play' in sys.argv:
        p1_win = 0
        p2_win = 0
        board = Board()
        # newStr = str(board)
        # print(str(board))

        player_turn = random.randint(1, 2)

        game_over = False
        first_turn = True
        first_round = True
        save_first_p = 100

        while True:
            print(str(board))
            print(f"CURRENT PLAYER'S TURN: {player_turn}")

            print("[=========== Your available moves ===========]")
            print(board.get_legal_moves(player_turn))
            print("========================================")

            curTurn = player_turn

            while curTurn == player_turn:
                # This should come in as a pair (piece, location)
                piece, userMove = input("Please select the move you want to make <piece#> <index#>: ").split()

                piece = int(piece)
                if piece != -1:  # -1 will be the optional termination command
                    userMove = int(userMove)

                    if piece < 0 or piece > 6:
                        print("Incorrect input!!")
                        userInput = -1

                    while userMove not in board.get_legal_moves(player_turn)[piece]:
                        print(f"current move: {piece} to {userMove}")
                        piece, userMove = input("That is not a valid piece move! Please retry!: ").split()
                        piece = int(piece)
                        userMove = int(userMove)

                    if board.execute_move(player_turn, piece, userMove) == True:
                        player_turn = (player_turn % 2) + 1

                else:
                    player_turn = (player_turn % 2) + 1

                if player_turn != curTurn:
                    print("SWITCHING TURNS!")
                else:
                    print("Continue turn?")
                    print(str(board))

            print("Done!")





