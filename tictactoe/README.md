# Tic Tac Toe

This project is a implementation of CS50 Artificial Intelligence with Python Porject 0b - TicTacToe

It uses the Minimax algorithm approach to choose the *optimal* move/action that the AI can play on it's turn.

While [**runner.py**](runner.py) is responsible for the actual game board rendering and switching turns between the computer and the player, [**tictactoe.py**](tictactoe.py) is responsible for the **minimax** algorithm function *per se* and all it's supporting functions:

* **parse_board(board)** - returns terminal(board), winner(board) and utility(board) context information when called by these.
* **initial_state()** - returns initial empty board.
* **player(board)** - returns player who plays turn.
* **actions(board)** - returns set of all possible actions for a given board.
* **result(board, action)** - returns the board that resulted from original board after action (move).
* **winner** - returns the winner of the game, if there is one.
* **terminal(board)** - returns True for if the game is over, and False if game still in play.
* **utility(board)**: - returns the *utility* value of a board indicating who won the game. 1 if X won, 0 for a tie and -1 if O won.
* **minimax(board)** - returns the optimal action for the AI to play in a given move.
* **max_value(state)** - feeds minimax(board) returning the maximum value for a given state (board).
* **min_value(state)** - feeds minimax(board) returning the minimum value for given a state (board).


Implemented by Luis Felipe Klaus 




