from time import time
from tkinter import messagebox

import tkinter as tk
from tkinter.font import BOLD

"""
Play TicTacToe!
This script allows you to play any size grid of TicTacToe with another person, now in a GUI!
Have fun!
"""

GAME_VALS = {
    'X': 1,
    'EMPTY': 0,
    'O': -1
}

COLORS = {
    "WindowBackground": "#7DB46C",
    "ButtonBackground": "#E7EBE0",
    "LabelBackground": "#ABD6DF",
    "XBackground": "#6CA1B4",
    "OBackground": "#B47F6C"
}

MAX_BOARD_SIZE = 10

class TicTacToeWindow:
    """Window to play TicTacToe on!
    """
    def __init__(self, root):
        self.root = root
        self.root.title("TicTacToe!")
        self.startScreen()
        self.ORIGINAL_BACKGROUND = self.root.cget("background")
    
    def startScreen(self):
        
        self.window = tk.Label(self.root, text="Let's Play TicTacToe!", font=("Helvetica", 35))
        self.window.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        self.size_input_label = tk.Label(self.root, text="Enter the width of the board you want to play: ", font=("Helvetica", 15))
        self.size_input_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.size_input_help = tk.Label(self.root,\
                                    text="""The width is equivalent to the amount of tiles on one side of the board.\nA typical TicTacToe board is 3 tiles wide.""",\
                                    font=("Helvetica", 15), relief="ridge")
        self.size_input_help.grid(row=2, columnspan=2, padx=5, pady=5)
        
        self.size_input = tk.Entry(self.root)
        self.size_input.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        self.size_capture = tk.Button(self.root, width=25, text="Let's Play!", font=("Helvetica", 15), command=self.getSizeOfBoard)
        self.size_capture.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
        self.root.bind('<Return>', self.getSizeOfBoard)
        self.size_input.focus()
        
    def getSizeOfBoard(self, event=None):
        """
        Get the user to provide the size of the board they want to play. Max size = MAX_BOARD_SIZE
        Inputs: N/A
        Outputs: 
            sizeOfBoard (int) = Length of one side of the TicTacToe board they wish to play on
        """
        SIZE_ERROR_MESSAGE = f"Please enter a valid positive size, max size {MAX_BOARD_SIZE}, min size 3."
        if not self.size_input.get().isdigit():
            messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
            return
        
        self.sizeOfBoard = self.size_input.get()
        try:
            if 3 <= int(self.sizeOfBoard) <= MAX_BOARD_SIZE:
                # Number is positive and greater than/equal to three, less than/inclusive of max board size.
                self.makeGameBoard(int(self.sizeOfBoard))
            
            else:
                messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
                return
            
        except ValueError:
            messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
            return
           
    def makeGameBoard(self, size_of_board):
        """
        Create a square set of buttons with side length equal to the user input of size.

        Args:
            size_of_board ([int]): [Length of one side of square of TicTacToe]
        """
        self.root.unbind('<Return>')
        self.root.configure(bg=COLORS["WindowBackground"])
        
         # First clear the board
        self.destroyRootWidgets()
        
        if size_of_board > 7:
            self.BUTTON_HEIGHT = 75
            self.BUTTON_WIDTH = 75
        else:
            self.BUTTON_HEIGHT = 100
            self.BUTTON_WIDTH = 100
        
        self.game_data = TicTacToeGame(size_of_board)
        self.gui_game_data = {}
        
        # Next, loop through and create a square of buttons
        for height in range(size_of_board):
            self.row = height
            for width in range(size_of_board):
                self.column = width
                
                self.tictactoe_button_frame = tk.Frame(self.root, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH)
                
                self.tictactoe_button = tk.Button(self.tictactoe_button_frame, text="+", font=("Helvetica", 30, BOLD),\
                                            state=tk.DISABLED, borderwidth=4, bg=COLORS["ButtonBackground"],\
                                            command=lambda coords=(self.row, self.column): self.gameButtonPressed(coords))
                self.tictactoe_button.grid(sticky="news")
                
                self.tictactoe_button_frame.grid(row=self.row, column=self.column, padx=5, pady=5)
                self.tictactoe_button_frame.rowconfigure(0, weight=1)
                self.tictactoe_button_frame.columnconfigure(0, weight=1)
                self.tictactoe_button_frame.grid_propagate(0)
                
                self.gui_game_data[(self.row, self.column)] = (self.tictactoe_button)
                self.game_data.addGameSpot((self.row, self.column))
        
        self.status_frame = tk.Frame(self.root, height=50)
        self.status_frame.grid(row=(self.row + 1), columnspan=(self.column+1), padx=5, pady=5, sticky="news")
        self.status_frame.rowconfigure(0, weight=1)
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.grid_propagate(0)
        
        self.find_first_player_button = tk.Button(self.status_frame, text='Click to roll to see if X or O is first!',\
                                            font=("Helvetica", 13, BOLD), borderwidth=3,\
                                            command=self.whichPlayerFirst)
        self.find_first_player_button.grid(sticky="news")
    
    def whichPlayerFirst(self):
        """[Runs TicTacToeGame method that returns 1 for X turn, or -1 for O turn]
        """        
        [vals.config(state="normal") for keys, vals in self.gui_game_data.items()]
        
        self.find_first_player_button.destroy()
        
        self.game_data.findFirstPlayer()

        self.status_label = tk.Label(self.status_frame, borderwidth=3, relief="groove", font=("Helvetica", 20, BOLD), bg=COLORS['LabelBackground'])
        self.status_label.grid(row=0, sticky="news")
        
        self.updateTurn()
        
    def gameButtonPressed(self, coords):
        """
        [Determines which button was pressed, via lambda function tied to button that produces a tuple of coordinates for pressed button]
        """
        self.coordinates_of_button = (coords[0], coords[1])
        self.button_pressed = self.gui_game_data[self.coordinates_of_button]
        self.button_pressed.config(state='disabled')
        self.button_pressed['text'] = self.current_turn_label
        
        if self.current_turn == GAME_VALS['X']:
            self.button_pressed['background'] = COLORS['XBackground']
        else:
            self.button_pressed['background'] = COLORS['OBackground'] 
            
        self.game_data.updateGameSpot(self.coordinates_of_button)
        self.game_data.updateTurnCount()
        
        if self.game_data.checkForWin(self.coordinates_of_button):
            self.gameOver()
        else:
            self.game_data.updateTurn()
            
            if not self.game_data.checkSpotsAvailable():
                self.gameOver(GAME_VALS['EMPTY'])
            else:
                self.updateTurn()
        
    def updateTurn(self):
        """Updates self.current_turn and self.current_turn_label with whoever's turn it is
        """
        self.current_turn = self.game_data.getTurn()
        self.current_turn_label = [key for key, val in GAME_VALS.items() if val==self.current_turn][0]
        
        self.status_label['text'] = f"{self.current_turn_label}'s turn!"
    
    def gameOver(self, who_won=None):
        """Updates the window with who won

        Args:
            who_won (integer): Refreshes board with whoever won

        """
        
        if who_won == GAME_VALS["EMPTY"]:
            winning_string = "Tie!"
        elif not who_won:
            winning_string = f"{self.current_turn_label} won!"
        
        self.status_label['text'] = winning_string
        
        self.play_again = tk.Button(self.root, text="Play Again?", command=self.playAgain)
        self.play_again.grid(row=(self.row + 2), columnspan = (self.column+1), padx=5, pady=5, sticky="news")
    
    def destroyRootWidgets(self):
         # First clear the board
        for widgets in self.root.winfo_children():
            widgets.destroy()
    
    def playAgain(self):
        self.destroyRootWidgets()
        self.root["background"] = self.ORIGINAL_BACKGROUND
        self.startScreen()
        
        
class TicTacToeGame(object):
    """[Manages the game data for TicTacToe]
    """
    def __init__(self, game_size):
        """Constructor. Starts empty game data dictionary, and initializes turn count.
        
        Args:
            game_size (integer): Assuming square board, length of one side of tictactoe board.
        """
        self.game_data = {}
        self.turn_count = 0
        self.game_size = game_size
    
    def addGameSpot(self, coordinates):
        """[Appends spot to self.game_data dictionary with key being coordinates of new spot, and value being EMPTY game value]

        Args:
            coordinates ([tuple]): Coordinates of spot to add
        """
        self.game_data[coordinates] = GAME_VALS["EMPTY"]
        
    def updateGameSpot(self, coordinates):
        """Updates the gamespot with either X's or O's spot

        Args:
            coordinates ([tuple]): Coordinates of spot to update
        """
        if self.turn == 1:
            # Was X's turn, update with X's marker
            self.game_data[coordinates] = GAME_VALS["X"]
        else:
            self.game_data[coordinates] = GAME_VALS["O"]
    
    def checkSpotsAvailable(self):
        """Checks if cat's game or not
        
        Returns:
            True (boolean): if spots available
            False (boolean): if spots not available
        """
        if self.turn_count >= self.game_size ** 2:
            return False
        else:
            return True
                 
    def findFirstPlayer(self):
        """Randomly get first player based on current time being even or odd.
        """
        if (round(time()) % 2) == 0:
            self.turn = GAME_VALS["X"]
        else:
            self.turn = GAME_VALS["O"]
        
    def updateTurnCount(self):
        """Update the turn count for this instance
        """
        self.turn_count += 1
        
    def updateTurn(self):
        """Update whose turn it is
        """
        if self.turn == GAME_VALS["X"]:
            self.turn = GAME_VALS["O"]
        else:
            self.turn = GAME_VALS["X"]
    
    def getTurn(self):
        """Getter for self.turn.
        
        Returns:
            self.turn (integer): 1 for X's turn, -1 for O's turn.
        """
        return self.turn
    
    def checkForWin(self, coordinates):
        """Checks if one of the player's won!

        Args:
            coordinates (tuple): Tuple of coordinates of location player chose
            
        Return:
            True (boolean): If there was a win
            False (boolean): If there as no win
        """
        
        if self.turn_count < (2 * self.game_size) - 1:
            return

        else:
        
            rows_check = set()
            col_check = set()
            diag_check = set()
            anti_diag_check = set()
            
            row = coordinates[0]
            col = coordinates[1]
            
            is_diagonal = self.checkIfDiagonal(row, col)
            
            
            for vals in range(self.game_size):
                rows_check.add(self.game_data[row, vals])
                col_check.add(self.game_data[vals, col])
                
                if is_diagonal:
                    diag_check.add(self.game_data[vals, vals])
                    anti_diag_check.add(self.game_data[vals, self.game_size-vals-1])
                
            if len(rows_check) == 1:
                if self.turn in rows_check:
                    return True
            elif len(col_check) == 1:
                if self.turn in col_check:
                    return True
            elif is_diagonal:
                if len(diag_check) == 1:
                    if self.turn in diag_check:
                        return True
                elif len(anti_diag_check) == 1:
                    if self.turn in anti_diag_check:
                        return True
            else:
                return False
               
    def checkIfDiagonal(self, row, col):
        """Checks if the coordinate user chose lie on a diagonal

        Args:
            row (int): Row coordinate of user chosen spot
            col (int): Column coordinate of user chosen spot
        """
        if (row == col) or (row + col == self.game_size - 1):
            return True
       
    
          
# def getFirstPlayer():
#     """ Randomly get first player based on current time being either even or odd """
#     if (round(time()) % 2) == 0:
#         print("X is first")
#         return GAME_VALS['X']
    
#     else:
#         print("O is first")
#         return GAME_VALS['O']    
# def main():
#     """
#     Take in an input from the user of the size of the board they want.
#     Create the board, initializing a dict with game data (key = coordinates, value = '_' (empty), 'X', or 'O')
#     Randomly choose who goes first.
#     Display the board initially.
#     Play the game, taking in user input for a location, redisplaying the board, and checking for a winning move.
#     """
#     while True:
#         try:
#             sizeOfBoard = 3
#             #sizeOfBoard = int(input("What size of square tictactoe board do you want to play on? "))
#             if 0 < sizeOfBoard <= MAX_BOARD_SIZE:
#                 # Number is positive and greater than zero, less than/inclusive of max board size.
#                 print(f"Square will be {sizeOfBoard} x {sizeOfBoard}")
#                 break
#             else:
#                 print(f"Please enter a whole, positive number, with a max size of {str(MAX_BOARD_SIZE)}.")

#         except ValueError:
#             print("Please enter a whole, positive number.")
#             continue

#     # Create data locations to play on
#     board_data = createGameLocs(sizeOfBoard)
#     # Create and display gameboard
#     displayGameBoard(sizeOfBoard, board_data)

#     # Roll the dice for who goes first
#     whichturn = getFirstPlayer()    # True if X, false if O

#     # Play the first turn of the game, asking for input of coordinates
#     playGame(whichturn, sizeOfBoard, board_data)
#     turn_counter = 0

#     while True:
#         turn_counter += 1
#         # Loop through the game, deciding who is next based on who came before
#         if whichturn == GAME_VALS['X']:
#             # X was first, now make O turn
#             whichturn = GAME_VALS['O']
            
#         else:
#             # O was first, now make X turn
#             whichturn = GAME_VALS['X']
            
#         row_played, col_played = playGame(whichturn, sizeOfBoard, board_data)
        
#         if turn_counter >= (2 * sizeOfBoard) - 1:
#             isWinner = checkWin(row_played, col_played, sizeOfBoard, board_data)

#             if isWinner:
#                 if whichturn == GAME_VALS['X']:
#                     print("Congratulations, X won!")
#                     break
#                 else:
#                     print("Congratulations, O won!")
#                     break
                
# def getSizeOfBoard():
#     """Get the user to provide the size of the board they want to play. Max size = MAX_BOARD_SIZE
#     Inputs: N/A
#     Outputs: 
#         sizeOfBoard (int) = Length of one side of the TicTacToe board they wish to play on
#     """
#     while True:
#         try:
#             sizeOfBoard = int(input("What size of square tictactoe board do you want to play on? "))
#             if 0 < sizeOfBoard <= MAX_BOARD_SIZE:
#                 # Number is positive and greater than zero, less than/inclusive of max board size.
#                 print(f"Square will be {sizeOfBoard} x {sizeOfBoard}")
#                 break
#             else:
#                 print(f"Please enter a whole, positive number, with a max size of {str(MAX_BOARD_SIZE)}.")

#         except ValueError:
#             print("Please enter a whole, positive number.")
#             continue
    
# def createGameLocs(boardSize):
#     """
#     Create data associated with each square on the TicTacToe board, based on board size

#     Input: boardSize(int)

#     Output: Dict {key = tuple of coordinates : value = '_', representing EMPTY}
#     """
#     start_board_data = {}
#     for rows in range(1, boardSize+1):
#         for cols in range(1, boardSize+1):
#             start_board_data[(rows, cols)] = GAME_VALS['EMPTY']

#     return start_board_data
    
# def displayGameBoard(boardSize, board_data):
#     """ Displays console view of current game board """
#     for rows in range(1, boardSize+1):
#         for cols in range(1, boardSize+1):
#             if cols != boardSize:
#                 print(f"| {board_data[(rows, cols)]} ", end="")

#             else:
#                 print(f"| {board_data[(rows, cols)]} |", end="")
#         print("")

# def getFirstPlayer():
#     """ Randomly get first player based on current time being either even or odd """
#     if (round(time()) % 2) == 0:
#         print("X is first")
#         return GAME_VALS['X']
    
#     else:
#         print("O is first")
#         return GAME_VALS['O']

# def playGame(xORo, boardSize, board_data):
#     """ 
#     Function intakes a users chosen location, and plays it.

#     Input:
#         xORo = char of X or O, based on whose turn it is
#         boardSize(int) = Length of one side of the board

#     Output: row(int) and col(int) played
#     """

#     if xORo == GAME_VALS['X']:
#         # X's turn
#         current_turn = GAME_VALS['X']
#     else:  
#         # O's turn
#         current_turn = GAME_VALS['O']
    
#     while True:
#         # Loop through user input
#         coords = input(f"Please enter coordinates (#, #) of a location to insert {GAME_VALS[current_turn]}: ")
        
#         try:
#             # First verify if inputs are indeed integers within the board size
#             row_played, col_played = parseCoords(coords, boardSize)
            
#             if checkSquares(row_played, col_played, board_data):
#                 # User input location is not currently in play, record and return to main()
#                 recordSquare(row_played, col_played, board_data, current_turn)
#                 displayGameBoard(boardSize, board_data)
#                 return row_played, col_played

#             else:
#                 print("Invalid spot. Please try again.")
#                 continue

#         except ValueError as e:
#             print(e)
#             continue

# def parseCoords(coordinates, boardSize):
#     """
#     Parses the coordinates input by the user
    
#     Inputs: coordinates(string) = user input of coordinates
#             boardSize(int) = length of one side of board

#     Verifies this input are valid integers contained within the given board size

#     Output: If valid, returns the row and col as ints
#             If not valid, raises a ValueError
#     """

#     #remove parentheses and spaces from the input
#     coordinates = coordinates.replace("(", "").replace(")", "").replace(" ", "")

#     # Validate user inputs by splitting row and col
#     try:
#         row, col = coordinates.split(",")
#     except ValueError:
#         # Something went very wrong with inputs
#         raise ValueError("Error inputting the coordinates. Please enter coordinates in the (#, #) format.")
#     if not row.isdigit() or not col.isdigit():
#         # User input something other than a digit
#         raise ValueError("Please enter positive integers only, in the (#, #) format.")
#     elif not 0 < int(col) <= boardSize or not 0 < int(row) <= boardSize:
#         # User input integers that are out of bounds
#         raise ValueError("Error. Input was outside of board size.")
    
#     return int(row), int(col) 

# def checkSquares(row, col, board_data):
#     """
#     Check if spot is already taken, given an input spot location

#     Input: row (int), col(int), board_data(dict of game data)
    
#     Output: True if square is empty, False if not
#     """
#     if board_data[row, col] != GAME_VALS['EMPTY']:
#         return False

#     else:
#         return True

# def recordSquare(row, col, board_data, current_turn):
#     """Record square chosen in board_data dict"""
#     board_data[row, col] = current_turn
#     return

# def checkWin(row, col, boardSize, board_data):
#     """
#     Checks the row/col/diagonal that the user's input is located on for a win

#     Input: row(int) and col(int) input by user 

#     Output: True if win, False if not

#     Win defined as a row, col, or diagonal containing all X or O
#     """
#     possibleWinners = {
#         'ROWS': set(),
#         'COLS': set(),
#         'DIAG': set(),
#         'ANTI_DIAG': set()
#     }

#     check_diagonals = isDiagonal(row, col, boardSize)

#     if check_diagonals:
#         anti_diag_column = boardSize

#     for location in range(1, boardSize + 1):
#         possibleWinners['ROWS'].add(board_data[row, location])
#         possibleWinners['COLS'].add(board_data[location, col])

#         if check_diagonals:
            
#             possibleWinners['DIAG'].add(board_data[location, location])
#             possibleWinners['ANTI_DIAG'].add(board_data[location, anti_diag_column])

#             anti_diag_column += -1

    
#     rows_cols_diags_with_one_val = [vals for keys, vals in possibleWinners.items() if len(vals) == 1]

#     if not rows_cols_diags_with_one_val:
#         # No rows/cols/diagonals with all X, O, or '_' (empty)
#         return False

#     elif rows_cols_diags_with_one_val[0].issubset(GAME_VALS['EMPTY']):
#         # A row/col/diagonal contains consistent EMPTY values
#         return False
    
#     else:
#         # A row/col/diagonal contains all X or O
#         return True

# def isDiagonal(row, col, boardSize):
    # """ Checks if a diagonal win possible based on user's input move """
    # if row == col or (row + col) == boardSize + 1:
    #     return True
    
    # else:
    #     # Does not lie on a column
    #     return False

if __name__ == "__main__":
    # print(
    # """
    # You are playing TicTacToe!\n\
    # The goal is to fill a row, column, or diagonal with only your pieces!.\n\
    # If neither you nor your opponent can create a winning pattern, it's a cat's game!\n\
    # Note, please consider top left corner to be postion 1 x 1.
    # """)
    root = tk.Tk()
    TicTacToeWindow(root)
    
    root.mainloop()
    # main()