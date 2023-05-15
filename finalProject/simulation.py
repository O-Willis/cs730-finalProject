import sys
import Arena
from chinesecheckers.CCheckersPlayers import *
from chinesecheckers.CCheckersGame import CCheckersGame as Game

if len(sys.argv) != 4:
    print("Usage:[-play <player1> <player2>]")
    exit(0)

# Initialize game
game = Game(6)
# Initializing players to be chosen
humanPlayer = HumanPlayer(game).play
randomPlayer = RandPlayer(game).play
minimaxPlayer = MinMaxPlayer(game).play
alphaPlayer = AlphaBetaPlayer(game).play
args = {'numMCTSSims': 60}
mcts = MCTSPlayer(game, args).play
mctsPlayer = mcts

# Choosing game player 1
print(f"\nAsked for Player 1 to be {sys.argv[2]}")
if sys.argv[2] == "human":
    player1 = humanPlayer
elif sys.argv[2] == "minimax":
    player1 = minimaxPlayer
elif sys.argv[2] == "alpha-beta":
    player1 = alphaPlayer
elif sys.argv[2] == "mcts":
    player1 = mctsPlayer
elif sys.argv[2] == "random":
    player1 = randomPlayer
else:
    print("\tNot proper player")
    print("\tUsage:[-play <player1> <player2>]")
    print("\tPlayers List: human, minimax, alpha-beta, mcts")
    exit(0)
print("\tPlayer 1 is correctly chosen.\n")

# Choosing game player 2
print(f"Asked for Player 2 to be {sys.argv[3]}")
if sys.argv[3] == "human":
    player2 = humanPlayer
elif sys.argv[3] == "minimax":
    player2 = minimaxPlayer
elif sys.argv[3] == "alpha-beta":
    player2 = alphaPlayer
elif sys.argv[3] == "mcts":
    player2 = mctsPlayer
elif sys.argv[3] == "random":
    player2 = randomPlayer
else:
    print("\tNot proper player.")
    print("\tUsage:[-play <player1> <player2>]")
    print("\tPlayers List: human, minimax, alpha-beta, mcts, random")
    exit(0)

print("\tPlayer 2 is correctly chosen.\n")

# Putting players into Arena, then fight begins...
arena = Arena.Arena(player1, player2, game, display=Game.display)

# Printing results
print(arena.playGame(verbose=True))