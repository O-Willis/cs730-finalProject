
# Minimax w/o pruning
python3 simulation.py -play 10 "mcts" "minimax"
python3 simulation.py -play 30 "mcts" "minimax"
python3 simulation.py -play 60 "mcts" "minimax"


# Minimax with pruning
python3 simulation.py -play 10 "mcts" "alpha-beta"
python3 simulation.py -play 30 "mcts" "alpha-beta"
python3 simulation.py -play 60 "mcts" "alpha-beta"

# MCTS
python3 simulation.py -play 10 "mcts" "mcts"
python3 simulation.py -play 30 "mcts" "mcts"
python3 simulation.py -play 60 "mcts" "mcts"