import sys
import os
import logging
import coloredlogs

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
    # print(f"Arguments count: {len(sys.argv)}")
    # if '-help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
    #     printHelp()





