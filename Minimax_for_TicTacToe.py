"""Small script to create and run test cases on writing the minimax algorithm for TicTacToe.

A few test cases will be generated that will have a random set of moves already used, based on a 3x3 board.

Will be successful when a computer player can see all possible options starting from the first move
The game board will be input as follows:

Type: Dict
{ (tuple) Coordinate of spot : (int) Value of current spot}

Value is -1 for O, 0 for EMPTY, 1 for X

Example for a 3x3:
{
    (0, 0) : -1,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 0
}

Which would look like:

O | - | -
- | - | -
- | - | -

"""

"""
Test Case: 0
Turn: X's
Moves to win: 1
Type of win: Diagonal

- | O | -
O | X | -
O | - | X

Test Case: 1
Turn: X's
Moves to win: 1
Type of win: Vertical

X | - | -
X | O | O
- | - | -

Test Case: 2
Turn: X's
Moves to win: 1
Type of win: Horizontal

O | O | -
- | - | -
X | - | X

Test Case: 3-5
Respectively identical to Test Cases 1-3, but O's are flipped

Test Case: 6
An empty board, computer goes first

Test Case: 7
Player has played a corner spot

Test Case: 8
Player has played a corner and middle spot, PC has played opposite corner
"""

TEST_CASES = [
{ #0
    (0, 0) : 0,
    (0, 1) : -1,
    (0, 2) : 0,
    (1, 0) : -1,
    (1, 1) : 1,
    (1, 2) : 0,
    (2, 0) : -1,
    (2, 1) : 0,
    (2, 2) : 1
},

{ #1
    (0, 0) : 1,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : 1,
    (1, 1) : -1,
    (1, 2) : -1,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 0
},

{ #2
    (0, 0) : -1,
    (0, 1) : -1,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : 1,
    (2, 1) : 0,
    (2, 2) : 1
},

{ #3
    (0, 0) : 0,
    (0, 1) : 1,
    (0, 2) : 0,
    (1, 0) : 1,
    (1, 1) : -1,
    (1, 2) : 0,
    (2, 0) : 1,
    (2, 1) : 0,
    (2, 2) : -1
},

{ #4
    (0, 0) : -1,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : -1,
    (1, 1) : 1,
    (1, 2) : 1,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 0
},

{ #5
    (0, 0) : 1,
    (0, 1) : 1,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : -1,
    (2, 1) : 0,
    (2, 2) : -1
},

{ #6
    (0, 0) : 0,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 0
},

{ #7
    (0, 0) : -1,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 0
},

{ #8
    (0, 0) : -1,
    (0, 1) : 0,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : -1,
    (1, 2) : 0,
    (2, 0) : 0,
    (2, 1) : 0,
    (2, 2) : 1
},

{ #9
    (0, 0) : -1,
    (0, 1) : -1,
    (0, 2) : 1,
    (1, 0) : -1,
    (1, 1) : -1,
    (1, 2) : 1,
    (2, 0) : 1,
    (2, 1) : 1,
    (2, 2) : 1
}]

GAME_VALS = {
    'X': 1,
    'EMPTY': 0,
    'O': -1
}


def minimax_score_this_turn(whose_turn, game_board, turn_count):
    """
    Implements minimax algorithm, reads in a TicTacToe gameboard, performs algorithm to find potential best move
    This involves determining whether best move is offensive or defensive
    It creates a 'game tree', with each branch being a different possible game option
    Scores assigned for gameboard positions:
    
    -10 for O win
    10 for X win
    Add # of turns to O score
    Subtract # of turns to X score
    
    Args:
        whose_turn (int) : -1 for O's turn, 1 for X's turn
        game_board (dict) : Keys = coordinates of spots, vals are -1 if O spot, 0 if EMPTY, 1 if X spot
        turn_count (int) : Initialized at 0, counts the # of turns needed for a win in order to find optimal move
    """

    if computer_check_for_win(3, game_board):
        if whose_turn == GAME_VALS["X"]:
            return -10, turn_count
        else:
            return 10, turn_count
        
    if not get_available_spaces(game_board):
        return 0, turn_count
    
    available_spaces = [coords for coords, vals in game_board.items() if vals == 0]
    scores = {}
    turns = {}
    for space in available_spaces:
        game_board[space] = whose_turn
        final_score, final_turn_count = minimax_score_this_turn(whose_turn * -1, game_board, turn_count + 1)
        scores[space] = final_score
        turns[space] = final_turn_count
        game_board[space] = 0
        
    if whose_turn == GAME_VALS["O"]:
        return min(scores.values()) + min(turns.values()), min(turns.values())
    else:
        return max(scores.values()) - min(turns.values()), min(turns.values())

def find_next_move(game_board, whose_turn):
    """
    Function runs each possible move available through MINIMAX algorithm to determine a score for the next move.

    Args:
        game_board (dict): Keys = coordinates of spots, vals are -1 if O spot, 0 if EMPTY, 1 if X spot
        whose_turn (int): -1 for O's turn, 1 for X's turn

    Returns:
        [tuple]: Coordinates of best available next move
    """

    available_moves = [coordinates for coordinates, value in game_board.items() if value == GAME_VALS["EMPTY"]]
    
    possible_final_moves = {}
    gameboard_for_next_move = game_board.copy()
    for moves in available_moves:
        gameboard_for_next_move[moves] = whose_turn
        score_for_this_turn, numb_of_turns = minimax_score_this_turn(whose_turn * -1, gameboard_for_next_move, 0)
        possible_final_moves[moves] = (score_for_this_turn, numb_of_turns)
        gameboard_for_next_move[moves] = 0
            
    return find_best_turn(possible_final_moves, whose_turn)

def find_best_turn(next_moves, whose_turn):
    """
    Given a list of best possible turns, find the best possible turn in the shortest amount of turn

    Args:
        next_moves (dict): Keys are next available moves, values are a tuple of (score, minimum move to win/loss)
        whose_turn (int) : -1 for O's turn, 1 for X's turn

    Returns:
        [tuple]: Coordinates of best possible move
    """
    
    if whose_turn == GAME_VALS["X"]:
        final_score = -1000
    else:
        final_score = 1000

    final_turns = 1000
    
    for coordinates, scores in next_moves.items():
        if whose_turn == GAME_VALS["X"] and scores[0] > final_score:
            
            final_coordinates = coordinates
            final_score = scores[0]
            final_turns = scores[1]
        
        elif whose_turn == GAME_VALS["O"] and scores[0] < final_score:
            final_coordinates = coordinates
            final_score = scores[0]
            final_turns = scores[1]   
                
        elif scores[0] == final_score:
            if scores[1] < final_turns:
                final_coordinates = coordinates
                final_turns = scores[1]
    
    return final_coordinates
            
def computer_check_for_win(game_size, game_board):
    """
    Function checks if the backtracking algorithm minimax produced a win, which is based on all possible move sets being run
    
    Args:
        game_size (int) : For minimax testing only, the size of one length of gameboard
        game_board (dict): The game board, with turns being added via minimax algorithm
        
        
    Returns:
        True (boolean): A win
        False (boolean): A loss
    """

    diag_check = set()
    anti_diag_check = set()

    for rows in range(game_size):
        rows_check = set()
        col_check = set()
        for cols in range(game_size):
            rows_check.add(game_board[rows, cols])
            col_check.add(game_board[cols, rows])
            
        if find_a_winner([rows_check, col_check]):
            return True

        diag_check.add(game_board[rows, rows])
        anti_diag_check.add(game_board[rows, game_size-rows-1])
    
    if find_a_winner([diag_check, anti_diag_check]):
        return True
        
    
    return False

def check_if_diagonal(row, col, game_size):
    """
    Checks if the coordinate user chose lie on a diagonal

    Args:
        row (int): Row coordinate of user chosen spot
        col (int): Column coordinate of user chosen spot
        game_size (int): Just for minimax testing, the length of one size of the gameboard
    
    Return:
        True (boolean): If lies on diagonal of board
        False (boolean): Does not lie on diagonal
    """

    if (row == col) or (row + col == game_size - 1):
        return True
    else:
        return False

def get_available_spaces(game_board):
    """
    Finds if there are available spaces left on the gameboard

    Args:
        game_board (dict): Keys are coordinates, values are -1 for O, 1 for X, 0 for empty
    
    Returns:
        True (boolean): If available spaces left
        False (boolean): If no available spaces
    """
    available_spaces = [coords for coords, vals in game_board.items() if vals == 0]
    if available_spaces:
        return True
    else:
        return False 

def find_a_winner(winner_checks):
    """
    Finds a winner from a set of given checks, checks being a win from a row, column, diagonal, or anti-diagonal
    
    Args:
        winner_checks (list) : A list of sets, 1 for each required
            These sets contain all unique values for the associated row/column/diagonal
            If a single set contains only one unique non-empty value (i.e. 1 or -1), then someone has won
    
    Return:
        True (boolean) : There was a winner
        False (boolean) : There was no winner
    
    """
    
    for checks in winner_checks:
        if len(checks) == 1:
            if 0 not in checks:
                return True
    
    return False

def displayGameBoard(game_size, game_board):
    
    for rows in range(game_size):
        for cols in range(game_size):
            value = [turn for turn, val in GAME_VALS.items() if val == game_board[(rows, cols)]]
            if value == ['EMPTY']:
                value = [""]
            print(value, end=" ")
        print("")
    coordinates = [coords for coords, values in game_board.items()]

if __name__ == "__main__":
    while True:
        try:
            test_case_to_run = int(input("Which test case: "))
            player = GAME_VALS[input("Which player: ")]
            next_move = find_next_move(TEST_CASES[test_case_to_run], player)
            print(f"Best move is {next_move}")
            TEST_CASES[test_case_to_run][next_move] = player
            displayGameBoard(3, TEST_CASES[test_case_to_run])
        except IndexError:
            print("Not a test case available to run.")
            continue
        except ValueError:
            print("Enter a valid integer test case.")
            continue
        except KeyError:
            print("X or O only")
            continue