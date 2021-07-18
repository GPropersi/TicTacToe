from time import time
from tkinter import messagebox
from tkinter.font import BOLD

import tkinter as tk
import random

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
    "ButtonBackground": "#9FA49E",
    "LabelBackground": "#ABD6DF",
    "XBackground": "#6CA1B4",
    "OBackground": "#B47F6C"
}

MAX_BOARD_SIZE = 10
BOARD_SIZES = list(range(3, MAX_BOARD_SIZE + 1))

class TicTacToeWindow:
    """Window to play TicTacToe on!
    """
    def __init__(self, root):
        """Constructor for TicTacToe game board

        Args:
            root (tkinter root objection): Main window for tkinter object to start tkinter GUI
        """
        self.root = root
        self.root.title("TicTacToe!")
        self.root.resizable(width=False, height=False)
        self.startScreen()
        self.ORIGINAL_BACKGROUND = self.root.cget("background") # Store original color for later during replay
    
    def startScreen(self):
        """Generates screen where user can choose width of TicTacToe they want to play on
        """        
        self.window = tk.Label(self.root, text="Let's Play TicTacToe!", font=("Helvetica", 35))
        self.window.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        self.player_option_frame = tk.LabelFrame(self.root, text="Choose Game Option", font=("Helvetica", 10))
        self.player_option_frame.grid(row=1, columnspan=2, padx=5, stick="news")
        
        self.player_option = tk.IntVar()
        self.comp_player_chk = tk.Radiobutton(self.player_option_frame, text="1 Player", font=("Helvetica", 13), variable=self.player_option, value=0)
        self.comp_player_chk.grid(row=0, column=0)
        
        self.two_player_chk = tk.Radiobutton(self.player_option_frame, text="2 Player", font=("Helvetica", 13), variable=self.player_option, value=1)
        self.two_player_chk.grid(row=0, column=1)
        
        self.player_option_frame.grid_columnconfigure(0, weight=1)
        self.player_option_frame.grid_columnconfigure(1, weight=1)
        
        self.size_input_label = tk.Label(self.root, text="Enter the width of the board you want to play: ", font=("Helvetica", 15))
        self.size_input_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.size_input = tk.Entry(self.root)
        self.size_input.grid(row=2, column=1, padx=5, pady=5)
        
        self.size_input_help = tk.Label(self.root,\
                                    text="""The width is equivalent to the amount of tiles on one side of the board.\n\n"""
                                            """A typical TicTacToe board is 3 tiles wide. Max width here is 10 tiles.\n\n"""
                                            """For 1-player, you are X.\n\n"""
                                            """For 2-player, decide who is X and who is O.""",\
                                    font=("Helvetica", 13), relief="ridge")
        self.size_input_help.grid(row=3, columnspan=2, padx=5, pady=5, ipadx=5, sticky="news")
        
        self.size_capture = tk.Button(self.root, width=25, text="Let's Play!", font=("Helvetica", 15), command=self.getSizeOfBoard, borderwidth=5)
        self.size_capture.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        
        self.root.bind('<Return>', self.getSizeOfBoard)
        self.size_input.focus()
        
    def getSizeOfBoard(self, event=None):
        """
        Get the user to provide the size of the board they want to play. Max size = MAX_BOARD_SIZE

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
            size_of_board (int): Length of one side of square of TicTacToe
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
        
        # Set single player or two player option
        self.setPlayerOptionInGame()
        
        self.gui_game_data = {}
        
        # Next, loop through and create a square of buttons
        for height in range(size_of_board):
            self.row = height
            for width in range(size_of_board):
                self.column = width
                
                self.tictactoe_button_frame = tk.Frame(self.root, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH)
                
                self.tictactoe_button = tk.Button(self.tictactoe_button_frame, text="", font=("Helvetica", 30, tk.font.BOLD),\
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
        """Runs TicTacToeGame method that returns 1 for X turn, or -1 for O turn
        """        
        [vals.config(state="normal") for keys, vals in self.gui_game_data.items()]
        
        self.find_first_player_button.destroy()
        
        self.game_data.findFirstPlayer()

        self.setStatusBarInGameWindow()
        
        self.updateTurn()
        
    def gameButtonPressed(self, coords):
        """Determines which button was pressed, via lambda function tied to button that produces a tuple of coordinates for pressed button.
        
        Args:
            coords (tuple): Defined as (row, column), both are integers
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
            # Check if winner value is equal to current turn's value
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
        
        if self.current_turn == GAME_VALS['O'] and self.player_option.get() == 0:
            print("The computer's turn!")
            self.computer_chosen_coords = self.game_data.randomMoveSupplier()
            self.gameButtonPressed(self.computer_chosen_coords)
              
    def gameOver(self, who_won=None):
        """Updates the window with who won

        Args:
            who_won (integer): Refreshes board with whoever won
                0 = Nobody, 1 = X, -1 = O
        """
        
        if who_won == GAME_VALS["EMPTY"]:
            winning_string = "Tie!"
        elif not who_won:
            winning_string = f"{self.current_turn_label} won!"
        
        self.status_label['text'] = winning_string
        
        self.play_again = tk.Button(self.root, text="Play Again?", command=self.playAgain)
        self.play_again.grid(row=(self.row + 2), columnspan = (self.column+1), padx=5, pady=5, sticky="news")
    
    def destroyRootWidgets(self):
        """Clears all widgets in self.root
        """
        for widgets in self.root.winfo_children():
            widgets.destroy()
    
    def playAgain(self):
        """Restarts GUI for a new round of playing
        """
        self.destroyRootWidgets()
        self.root["background"] = self.ORIGINAL_BACKGROUND
        self.startScreen()
    
    def setPlayerOptionInGame(self):
        """Gets the player option, sets up the game instance up for AI or 2 player game

        Sets TicTacToeGame.computer_player to:
            True (boolean): True if 1 player game [default is False for two player game]
        """
        if self.player_option.get() == 0:
            print("You want a one player game with the computer!")
            self.game_data.computer_player = True
   
    def setStatusBarInGameWindow(self):
        """Sets the status bar in the game window
        """
        self.status_label = tk.Label(self.status_frame, borderwidth=3, relief="groove", font=("Helvetica", 20, BOLD), bg=COLORS['LabelBackground'])
        self.status_label.grid(row=0, sticky="news")

class TicTacToeGame:
    """Manages the game data for TicTacToe
    """
    def __init__(self, game_size):
        """Constructor. Starts empty game data dictionary, and initializes turn count.
        
        Args:
            game_size (integer): Assuming square board, length of one side of tictactoe board.
            comp_player (boolean): True if 1 player, False if 2 player
        """
        self.game_data = {}
        self.turn_count = 0
        self.game_size = game_size
        self.computer_player = False
    
    def setPlayer(self, computer_player):
        """Setter for player option

        Args:
            computer_player (boolean): True for an AI player, False for 2 player
        """
        self.computer_player = computer_player
    
    def addGameSpot(self, coordinates):
        """[Appends spot to self.game_data dictionary with key being coordinates of new spot, and value being EMPTY game value]

        Args:
            coordinates (tuple): Coordinates of spot to add
        """
        self.game_data[coordinates] = GAME_VALS["EMPTY"]
        
    def updateGameSpot(self, coordinates):
        """Updates the gamespot with either X's or O's spot

        Args:
            coordinates (tuple): Coordinates of spot to update
        """
        if self.turn == 1:
            # Was X's turn, update with X's marker
            self.game_data[coordinates] = GAME_VALS["X"]
        else:
            self.game_data[coordinates] = GAME_VALS["O"]
    
    def checkSpotsAvailable(self):
        """Checks if cat's game or not by tracking move counts
        
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
        """Update the turn count for this instance via updating self.turn_count
        """
        self.turn_count += 1
        
    def updateTurn(self):
        """Update whose turn it is via updating self.turn
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
    
    def computerCheckForWin(self, game_board):
        """Function checks if the backtracking algorithm minimax produced a win, which is based on all possible move sets being run
        
        Args:
            game_board (dict): The game board, with turns being added via minimax algorithm
            
        Returns:
            True (boolean): A win
            False (boolean): A loss
        """
        rows_check = set()
        col_check = set()
        diag_check = set()
        anti_diag_check = set()
        
        for rows in range(self.game_size):
            for cols in range(self.game_size):
                rows_check.add(self.game_board[rows, cols])
                col_check.add(self.game_board[cols, rows])

            diag_check.add(self.game_board[rows, rows])
            anti_diag_check.add(self.game_board[rows, self.game_size-rows-1])
            
        if len(rows_check) == 1:
            if GAME_VALS['EMPTY'] not in rows_check:
                return True
        elif len(col_check) == 1:
            if GAME_VALS['EMPTY'] not in col_check:
                return True
        elif len(diag_check) == 1:
            if GAME_VALS['EMPTY'] not in diag_check:
                return True          
        elif len(anti_diag_check) == 1:
            if GAME_VALS['EMPTY'] not in anti_diag_check:
                return True
        
        else:
            return False
    
    def checkForWin(self, coordinates):
        """Checks if one of the player's won! Reads in the current instance's gameboard.
        Only checks for diagonal win if coordinates chosen lie on a diagonal.

        Args:
            coordinates (tuple): Tuple of coordinates of location player chose
            
        Returns:
            True (boolean): A win
            False (boolean): A loss
        """
        
        if self.turn_count < (2 * self.game_size) - 1:
            # Not enough moves to win a game
            return

        else:
            
            self.game_board = self.game_data.copy()
                
            rows_check = set()
            col_check = set()
            diag_check = set()
            anti_diag_check = set()

            row = coordinates[0]
            col = coordinates[1]
            
            is_diagonal = self.checkIfDiagonal(row, col)
            
            for vals in range(self.game_size):
                rows_check.add(self.game_data[(row, vals)])
                col_check.add(self.game_data[(vals, col)])
                
                if is_diagonal:
                    diag_check.add(self.game_board[(vals, vals)])
                    anti_diag_check.add(self.game_board[(vals, self.game_size-vals-1)])
            
            # Checks if current turn is only value in set, and not just EMPTY
            if len(rows_check) == 1:
                if self.turn in rows_check:                   
                    return True
            elif len(col_check) == 1:
                if self.turn in col_check:
                    return True
            elif is_diagonal:
                # Only checks for diagonal win if spot chosen is on a diagonal
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
        
        Return:
            True (boolean): If lies on diagonal of board (or anti-diagonal)
            False (boolean): Does not lie on diagonal (or anti-diagonal)
        """
        if (row == col) or (row + col == self.game_size - 1):
            return True
        else:
            return False
       
    def randomMoveSupplier(self):
        """Provides a random set of coordinates for the computer to choose 
        
        Return:
            A tuple of coordinates that are currently unoccupied
        """

        self.empty_spots = [coords for coords, vals in self.game_data.items() if vals == GAME_VALS["EMPTY"]]
        
        return random.choice(self.empty_spots)

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeWindow(root)  
    root.mainloop()
