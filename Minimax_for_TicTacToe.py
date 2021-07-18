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
Test Case: 1
Turn: X's
Moves to win: 1
Type of win: Diagonal

- | O | -
O | X | -
O | - | X

Test Case: 2
Turn: X's
Moves to win: 1
Type of win: Vertical

X | - | -
X | O | O
- | - | -

Test Case: 3
Turn: X's
Moves to win: 1
Type of win: Horizontal

O | O | -
- | - | -
X | - | X

Test Case: 4-6
Respectively identical to Test Cases 1-3, but O's turn
"""

TEST_CASES = [
{ #1
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

{ #2
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

{ #3
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

{ #4
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

{ #5
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

{ #6
    (0, 0) : 1,
    (0, 1) : 1,
    (0, 2) : 0,
    (1, 0) : 0,
    (1, 1) : 0,
    (1, 2) : 0,
    (2, 0) : -1,
    (2, 1) : 0,
    (2, 2) : -1
}]



def findBestTurn(whose_turn, game_board):
    """Needs to implement minimax algorithm, reads in the current TicTacToe gameboard, performs algorithm to find potential best move
    This involves determining whether best move is offensive or defensive
    If there are multiple best movies, it will randomly choose the best
    Scores assigned for gameboard positions:
    
    -10 for O win
    10 for X win
    Add # of turns to O score
    Subtract # of turns to X score
    
    Args:
        whose_turn (int) : -1 for O's turn, 1 for X's turn
        game_board (dict) : Keys = coordinates of spots, vals are -1 if O spot, 0 if EMPTY, 1 if X spot
    """
    # NEED: Turn counter, turn list that remembers turns played (via append)
    # Run check win here as base case
    
    # if not check win,
        # if X's turn, place an X
            # return newly_edited_gameboard, turn_counter, turn_list, whose_turn
        # elif O's turn, place an O
            # return newly_edited_gameboard, turn_counter, turn_list, whose_turn
    
    # really just want a list of all possible move options with a score attached, ready for parsing later
    
    available_spaces = [coords for coords, vals in game_board.items() if vals == 0]
    
    for space in available_spaces:
        print("minimax", space)
    
    print("here")
    
    '''
    Steps:
    1) Provide the minimax function a gameboard with an available space played (via for loop)
        ... but how to do recursion here
    
    1) Recursive function - first provide the game board at current state
    2) Base case is a win, loss, or tie
    3) If none of those, rerun the function with the next turn and next available space taken
    4) Count the turns needed to reach an end state
    
    '''
    
if __name__ == "__main__":
    findBestTurn(1, TEST_CASES[0])