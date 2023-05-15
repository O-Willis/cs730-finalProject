
# Minimax w/o pruning
echo "Running MCTS vs MiniMax iter = 10"
python3 simulation.py -play 10 "mcts" "minimax"
# currently at:
#       P1 : 2    P2: 8

# Minimax with pruning
echo "Running MCTS vs Alpba-Beta iter = 10"
python3 simulation.py -play 10 "mcts" "alpha-beta"
# currently at:
#       P1 : 2    P2: 8

# MCTS
echo "Running MCTS vs MCTS iter = 10"
python3 simulation.py -play 10 "mcts" "mcts"



echo "Running MCTS vs MiniMax iter = 30"
python3 simulation.py -play 30 "mcts" "minimax"

echo "Running MCTS vs Alpba-Beta iter = 30"
python3 simulation.py -play 30 "mcts" "alpha-beta"

echo "Running MCTS vs MCTS iter = 30"
python3 simulation.py -play 30 "mcts" "mcts"



echo "Running MCTS vs MiniMax iter = 50"
python3 simulation.py -play 50 "mcts" "minimax"

echo "Running MCTS vs Alpba-Beta iter = 50"
python3 simulation.py -play 50 "mcts" "alpha-beta"

echo "Running MCTS vs MCTS iter = 50"
python3 simulation.py -play 50 "mcts" "mcts"
