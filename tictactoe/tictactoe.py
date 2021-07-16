"""
Tic Tac Toe Player
"""

# TODO delethe this


import math
import copy

X = "X"
O = "O"
EMPTY = None

# Auxiliar function

def parse_board(board, function):
    """
    Parses board and feeds the calling-function with requested data 
    """
    # Check rows for a terminal state
    for row in board:
        is_terminal_state = len(row) > 0 and all(elem == row[0] for elem in row) and row[0] != EMPTY  

        if is_terminal_state and function == "terminal":
            return True

        if is_terminal_state and function == "winner":
            winner = row[0]
            return winner

        if is_terminal_state and function == "utility":
            if row[0] == X:
                return 1
            else:
                return -1         

    # Check columns for a terminal state
    inverted_board = [[], [], []]

    for row in board:
        for col in range(len(row)):
            inverted_board[col].append(row[col])
    
    for row in inverted_board:
        is_terminal_state = len(row) > 0 and all(elem == row[0] for elem in row) and row[0] != EMPTY  
        
        if is_terminal_state and function == "terminal":
            return True

        if is_terminal_state and function == "winner":
            winner = row[0]
            return winner
        
        if is_terminal_state and function == "utility":
            if row[0] == X:
                return 1
            else:
                return -1

    # Check diagonals for a terminal state]
    diagonals = [[], []]
    
    for i in range(len(board)):      
        for j in range(len(board[i])):  
            if i == j:
                diagonals[0].append(board[i][j])
            
            if len(board) - 1 - i == j:
                diagonals[1].append(board[i][j])

    for row in diagonals:
        is_terminal_state = len(row) > 0 and all(elem == row[0] for elem in row) and row[0] != EMPTY  
        
        if is_terminal_state and function == "terminal":
            return True

        if is_terminal_state and function == "winner":
            winner = row[0]
            return winner
        
        if is_terminal_state and function == "utility":
            if row[0] == X:
                return 1
            else:
                return -1

    # Check board for terminal state (tie - no winner)
    countEMPTY = 0

    for row in board:
        for col in row:
            if col == EMPTY:
                countEMPTY += 1
    
    if countEMPTY == 0 and function == "terminal":   
        return True
   
    if countEMPTY == 0 and function == "winner":
        return None
    
    if countEMPTY == 0 and function == "utility":
        return 0

    # Any other case 
    return False
    

def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialize EMPTY counter
    EMPTY_count = 0

    # Count number of empty spaces 
    for row in board:
        for col in row:
            if col == EMPTY:
                EMPTY_count += 1
    
    # Return X for a even and O for an odd count 
    if EMPTY_count % 2 != 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                available_actions.add((i,j))

    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Exception in case of not valid action
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Action not valid!")

    # Retrieve active player and add action to board
    add_move = player(board)
    # Use deepcopy board to ensure original board state integrity
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = add_move

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return parse_board(board, "winner")


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return parse_board(board, "terminal")
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return parse_board(board, "utility")


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        None

    available_actions = actions(board)

    # Call function according to algorithm's targert (MIN or MAX)
    if player(board) == X:
        V = -math.inf      
        optimal_action = tuple()

        for action in available_actions:
            min_v = min_value(result(board, action))
            if min_v > V:
                V = min_v
                optimal_action = action
                if V == 1:
                    return optimal_action
        
        return optimal_action
    
    # player(board) == O
    else: 
        V = math.inf
        optimal_action = tuple()      
        
        for action in available_actions:
            max_v = max_value(result(board, action))
            if max_v < V:
                V = max_v
                optimal_action = action
                if V == -1:
                    return optimal_action
        
        return optimal_action


def max_value(state):
    v = -math.inf

    if terminal(state):
        return utility(state)

    for action in actions(state):
        min_v = min_value(result(state, action))
        if min_v > v:
            v = min_v
            optimal_action = action
            if v == 1:
                return v
    
    return v


def min_value(state):
    v = math.inf
     
    if terminal(state):
        return utility(state)

    for action in actions(state):
        max_v = max_value(result(state, action))
        if max_v < v:
            v = max_v
            optimal_action = action
            if v == -1:
                return v
 
    return v
