from time import time
from tkinter import messagebox
from tkinter.font import BOLD
from math import ceil
from functools import wraps

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
    "X_LabelBackground": "#ABD6DF",
    "O_LabelBackground": "#E5D3CD",
    "XBackground": "#6CA1B4",
    "OBackground": "#B47F6C"
}

MAX_BOARD_SIZE = 10
BOARD_SIZES = list(range(3, MAX_BOARD_SIZE + 1))

class TicTacToeWindow:
    """Window to play TicTacToe on!"""

    def __init__(self, root):
        """Constructor for TicTacToe game board

        Args:
            root (tk.Tk()): Main window for tkinter object to start tkinter GUI
        """

        self.root = root
        self.root.title("TicTacToe!")
        self.root.resizable(width=False, height=False)
        self.start_screen()
        self.original_background = self.root.cget("background") # Store original color for later during replay
    
    def start_screen(self):
        """Generates screen where user can choose width of TicTacToe they want to play on"""

        self.window = tk.Label(self.root, text="Let's Play TicTacToe!", font=("Helvetica", 35))
        self.window.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        self.opponent_option_frame = tk.LabelFrame(self.root, text="Choose Opponent Option", font=("Helvetica", 10))
        self.opponent_option_frame.grid(row=1, columnspan=2, padx=5, stick="news")
        
        self.opponent_option = tk.IntVar()
        self.comp_player_chk = tk.Radiobutton(self.opponent_option_frame, text="1 Player", font=("Helvetica", 13), variable=self.opponent_option, value=0)
        self.comp_player_chk.grid(row=0, column=0)
        
        self.two_player_chk = tk.Radiobutton(self.opponent_option_frame, text="2 Player", font=("Helvetica", 13), variable=self.opponent_option, value=1)
        self.two_player_chk.grid(row=0, column=1)
        
        self.opponent_option_frame.grid_columnconfigure(0, weight=1)
        self.opponent_option_frame.grid_columnconfigure(1, weight=1)
        
        self.size_input_label = tk.Label(self.root, text="Enter the width of the board you want to play: ", font=("Helvetica", 15))
        self.size_input_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.size_input = tk.Entry(self.root)
        self.size_input.grid(row=2, column=1, padx=5, pady=5)
        
        self.size_input_help = tk.Label(self.root,\
                                    text="""The width is equivalent to the amount of tiles on one side of the board.\n\n"""
                                            """A typical TicTacToe board is 3 tiles wide. Max width here is 10 tiles.\n\n"""
                                            """Player 1 will decide if they are X or O.\n\n"""
                                            """The computer or Player 2 will be whichever is left.""",\
                                    font=("Helvetica", 13), relief="ridge")
        self.size_input_help.grid(row=3, columnspan=2, padx=5, pady=5, ipadx=5, sticky="news")
        
        self.size_capture = tk.Button(self.root, width=25, text="Let's Play!", font=("Helvetica", 15), command=self.get_player_choice, borderwidth=5)
        self.size_capture.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        
        self.root.bind('<Return>', self.get_player_choice)
        self.size_input.focus()
    
    def get_player_choice(self, event=None):
        """Make Player 1 choose if they want to play as X or O. Player 2 or the AI will take what is leftover"""
        
        if not self.get_size_of_board():
            # Size of board not input correctly
            return
        
        self.size_of_board = int(self.size_of_board)
        
        self.comp_player_chk["state"] = "disabled"
        self.two_player_chk["state"] = "disabled"
        self.size_capture["state"] = "disabled"
        self.size_input["state"] = "disabled"

        self.player_option_frame = tk.LabelFrame(self.root, text="Player 1, Choose X or O", font=("Helvetica", 10))
        self.player_option_frame.grid(row=5, columnspan=2, padx=5, sticky="news")
        
        self.player_one_x_or_o = tk.IntVar()
        self.x_player = tk.Radiobutton(self.player_option_frame, text="X", font=("Helvetica", 13), variable=self.player_one_x_or_o, value=GAME_VALS['X'])
        self.x_player.grid(row=0, column=0)
        
        self.o_player = tk.Radiobutton(self.player_option_frame, text="O", font=("Helvetica", 13), variable=self.player_one_x_or_o, value=GAME_VALS['O'])
        self.o_player.grid(row=0, column=1)
        
        self.player_option_frame.grid_columnconfigure(0, weight=1)
        self.player_option_frame.grid_columnconfigure(1, weight=1)
        
        self.start_button = tk.Button(self.root, width=25, text="Start!", font=("Helvetica", 15), command=self.start_game, borderwidth=5)
        self.start_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def start_game(self):
        """
        Checks if user chose X or O. If not, make them re-enter. If they did, start the game!
        """

        if not self.player_one_x_or_o.get():
            messagebox.showerror("Error", "Please choose X or O.")
        else:
            self.make_game_board()

        self.game_is_over = False

        
    def get_size_of_board(self):
        """
        Get the user to provide the size of the board they want to play. Max size = MAX_BOARD_SIZE

        Returns: 
            True (boolean) : Size of board was a valid integer between and including 3 and 10
            False (boolean) : Size was not valid
        """

        SIZE_ERROR_MESSAGE = f"Please enter a valid positive size, max size {MAX_BOARD_SIZE}, min size 3."
        if not self.size_input.get().isdigit():
            messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
            return False
        
        size_of_board = self.size_input.get()
        try:
            if 3 <= int(size_of_board) <= MAX_BOARD_SIZE:
                # Number is positive and greater than/equal to three, less than/inclusive of max board size.
                self.size_of_board = int(size_of_board)
                return True
            
            else:
                messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
                return False
            
        except ValueError:
            messagebox.showerror("Error", SIZE_ERROR_MESSAGE)
            return False
           
    def make_game_board(self):
        """Create a square set of buttons with side length equal to the user input of size."""

        self.root.unbind('<Return>')
        self.root.configure(bg=COLORS["WindowBackground"])
        
         # First clear the board
        self.destroy_root_widgets()
        
        if self.size_of_board > 7:
            self.BUTTON_HEIGHT = 75
            self.BUTTON_WIDTH = 75
        else:
            self.BUTTON_HEIGHT = 100
            self.BUTTON_WIDTH = 100
        
        self.game_data = TicTacToeGame(self.size_of_board)
        
        # Set single player or two player option
        self.set_player_option_in_game()
        
        self.gui_game_data = {}
        
        # Next, loop through and create a square of buttons
        for height in range(self.size_of_board):
            self.row = height
            for width in range(self.size_of_board):
                self.column = width
                
                self.tictactoe_button_frame = tk.Frame(self.root, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH)
                
                self.tictactoe_button = tk.Button(self.tictactoe_button_frame, text="", font=("Helvetica", 30, tk.font.BOLD),\
                                            state=tk.DISABLED, borderwidth=4, bg=COLORS["ButtonBackground"],\
                                            command=lambda coords=(self.row, self.column): self.game_button_pressed(coords))
                self.tictactoe_button.grid(sticky="news")
                
                self.tictactoe_button_frame.grid(row=self.row, column=self.column, padx=5, pady=5)
                self.tictactoe_button_frame.rowconfigure(0, weight=1)
                self.tictactoe_button_frame.columnconfigure(0, weight=1)
                self.tictactoe_button_frame.grid_propagate(0)
                
                self.gui_game_data[(self.row, self.column)] = (self.tictactoe_button)
                self.game_data.add_game_spot((self.row, self.column))
        
        self.status_frame = tk.Frame(self.root, height=50)
        self.status_frame.grid(row=(self.row + 1), columnspan=(self.column+1), padx=5, pady=5, sticky="news")
        self.status_frame.rowconfigure(0, weight=1)
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.grid_propagate(0)
        
        self.find_first_player_button = tk.Button(self.status_frame, text='Click to roll to see if X or O is first!',\
                                            font=("Helvetica", 13, BOLD), borderwidth=3,\
                                            command=self.which_player_first)
        self.find_first_player_button.grid(sticky="news")
    
    def which_player_first(self):
        """Runs TicTacToeGame method that returns 1 for X turn, or -1 for O turn"""       

        [vals.config(state="normal") for _, vals in self.gui_game_data.items()]
        
        self.find_first_player_button.destroy()
        
        self.game_data.find_first_player()

        self.set_status_bar_in_game_window()
        
        self.update_turn()
        
    def game_button_pressed(self, coords: tuple):
        """
        Determines which button was pressed, via lambda function tied to button that produces a tuple of coordinates for pressed button.
        
        Args:
            coords (tuple): Defined as (row, column), both are integers
        """
        if self.game_is_over:
            return
            
        self.coordinates_of_button = (coords[0], coords[1])
        self.button_pressed = self.gui_game_data[self.coordinates_of_button]
        self.button_pressed.config(state='disabled')
        self.button_pressed['text'] = self.current_turn_label
        
        if self.current_turn == GAME_VALS['X']:
            self.button_pressed['background'] = COLORS['XBackground']
        else:
            self.button_pressed['background'] = COLORS['OBackground'] 
            
        self.game_data.update_game_spot(self.coordinates_of_button)
        self.game_data.update_turn_count()
        
        if self.game_data.player_check_for_win(self.coordinates_of_button):
            # Check if winner value is equal to current turn's value
            self.game_over()
        else:
            self.game_data.update_turn()
            
            if self.game_data.get_turn_count() > (self.size_of_board * 2) + 2:
                if not self.game_data.check_if_win_possible():
                    self.game_over(possible_moves=False)
                    return
            
            if not self.game_data.check_spots_available():
                self.game_over(GAME_VALS['EMPTY'])
            else:
                self.update_turn()
        
    def update_turn(self):
        """
        Updates self.current_turn and self.current_turn_label with whoever's turn it is.
        
        Runs the computer's turn if applicable
        """
        
        self.current_turn = self.game_data.get_turn()
        self.current_turn_label = [label for label, value in GAME_VALS.items() if value == self.current_turn]
        
        if self.current_turn == self.player_one_x_or_o.get():
            self.status_label['text'] = "Player 1's turn!"
        elif self.current_turn != self.player_one_x_or_o.get() and self.opponent_option.get() == 1:
            self.status_label['text'] = "Player 2's turn!"
        
        self.set_status_bar_background_color(self.current_turn)
        
        # Let the computer play
        if self.opponent_option.get() == 0:
            # AI player
            if self.current_turn == self.player_one_x_or_o.get():
                # Player's turn
                return
            else:
                self.computer_chosen_coords = self.game_data.find_next_move_for_computer()
                self.game_button_pressed(self.computer_chosen_coords)
      
    def game_over(self, who_won=None, possible_moves=True):
        """
        Updates the window with who won

        Args:
            who_won (integer): Refreshes board with whoever won
                0 = Nobody, 1 = X, -1 = O
        """
        
        if who_won == GAME_VALS["EMPTY"]:
            winning_string = "Tie!"
        elif possible_moves is False:
            winning_string = "No winning moves left. Tie!"
            if self.size_of_board == 3:
                self.status_label['font'] = ("Helvetica", 17, BOLD)
        elif not who_won and possible_moves is True:
            if self.current_turn == self.player_one_x_or_o.get():
                winning_string = "Player 1 Won!"
            else:
                if self.opponent_option.get() == 0:
                    winning_string = "The Computer Won!"
                else:
                    winning_string = "Player 2 Won!"
        
        self.status_label['text'] = winning_string
        
        self.play_again_button = tk.Button(self.root, text="Play Again?", command=self.play_again)
        self.play_again_button.grid(row=(self.row + 2), columnspan = (self.column+1), padx=5, pady=5, sticky="news")
        self.game_is_over = True
    
    def destroy_root_widgets(self):
        """Clears all widgets in self.root"""

        for widgets in self.root.winfo_children():
            widgets.destroy()
    
    def play_again(self):
        """Restarts GUI for a new round of playing"""

        self.destroy_root_widgets()
        self.root["background"] = self.original_background
        self.start_screen()
    
    def set_player_option_in_game(self):
        """
        Gets the player option, sets up the game instance up for AI or 2 player game

        Sets TicTacToeGame.computer_player to:
            True (boolean): True if 1 player game [default is False for two player game]
        """

        if self.opponent_option.get() == 0:
            self.game_data.computer_player = True
   
    def set_status_bar_in_game_window(self):
        """Sets the status bar in the game window"""

        self.status_label = tk.Label(self.status_frame, borderwidth=3, relief="groove", font=("Helvetica", 20, BOLD))
        self.status_label.grid(row=0, sticky="news")
        
        self.set_status_bar_background_color(self.game_data.get_turn())

    def set_status_bar_background_color(self, turn):
        """
        Sets the background color of the status label in the game

        Args:
            turn (int): -1 for O's turn, 1 for X's turn
        """
        
        if turn == GAME_VALS['X']:
            self.status_label["bg"] = COLORS['X_LabelBackground']
        else:
            self.status_label["bg"] = COLORS['O_LabelBackground']
    
class TicTacToeGame:
    """Manages the game data for TicTacToe"""

    def __init__(self, game_size: int):
        """
        Constructor. Starts empty game data dictionary, and initializes turn count.
        
        Args:
            game_size (integer): Assuming square board, length of one side of tictactoe board.
        """

        self.game_data = {}
        self.turn_count = 0
        self.game_size = game_size
        self.computer_player = False

        if self.game_size == 3:
            self.max_minimax_depth = self.game_size ** 2
        elif 4 <= self.game_size <= 7:
            self.max_minimax_depth = (-self.game_size + 9)
        elif self.game_size == 8:
            self.max_minimax_depth = 2
        else:
            self.max_minimax_depth = 1
    
    def set_player(self, computer_player: bool):
        """
        Setter for player option

        Args:
            computer_player (boolean): True for an AI player, False for 2 player
        """

        self.computer_player = computer_player
    
    def add_game_spot(self, coordinates: tuple):
        """
        Appends spot to self.game_data dictionary with key being coordinates of new spot, and value being EMPTY game value

        Args:
            coordinates (tuple): Coordinates of spot to add
        """

        self.game_data[coordinates] = GAME_VALS["EMPTY"]
        
    def update_game_spot(self, coordinates):
        """
        Updates the gamespot with either X's or O's spot

        Args:
            coordinates (tuple): Coordinates of spot to update
        """

        if self.turn == 1:
            # Was X's turn, update with X's marker
            self.game_data[coordinates] = GAME_VALS["X"]
        else:
            self.game_data[coordinates] = GAME_VALS["O"]
    
    def check_spots_available(self, game_board=None):
        """
        Checks if cat's game or not by tracking move counts, or checking available moves on gameboard
        
        Returns:
            True (boolean): if spots available
            False (boolean): if spots not available
        """
        
        if self.turn_count >= self.game_size ** 2:
            return False
        
        if game_board:
            available_spaces = [coords for coords, vals in game_board.items() if vals == GAME_VALS["EMPTY"]]
    
        else:
            available_spaces = [coords for coords, vals in self.game_data.items() if vals == 0]

        if available_spaces:
            return True

        else:
            return False
    
    def check_if_win_possible(self):
        """
        Check if a win is even possible - if all rows, columns, and diagonals contain one of each X and O, no wins are possible.
        
        If game_tied_count == (Length of board * 2) + 2, True
        
        Returns:
            True (boolean) : If win is still possible
            False (boolean) : If win is not possible
        """
        
        diag_check = set()
        anti_diag_check = set()
        game_board = self.game_data
        game_tied_count = 0

        for rows in range(self.game_size):
            rows_check = set()
            col_check = set()
            for cols in range(self.game_size):
                rows_check.add(game_board[rows, cols])
                col_check.add(game_board[cols, rows])
                
            if GAME_VALS['X'] in rows_check and GAME_VALS['O'] in rows_check:
                game_tied_count += 1
            
            if GAME_VALS['X'] in col_check and GAME_VALS['O'] in col_check:
                game_tied_count += 1
                

            diag_check.add(game_board[rows, rows])
            anti_diag_check.add(game_board[rows, self.game_size-rows-1])
        
        if GAME_VALS ['X'] in diag_check and GAME_VALS['O'] in diag_check:
            game_tied_count += 1
        
        if GAME_VALS['X'] in anti_diag_check and GAME_VALS['O'] in anti_diag_check:
            game_tied_count += 1
            
        if game_tied_count >= (self.game_size * 2) + 2:
            return False
        else:
            return True
               
    def find_first_player(self):
        """Randomly get first player based on current time being even or odd"""

        if (round(time()) % 2) == 0:
            self.turn = GAME_VALS["X"]
        else:
            self.turn = GAME_VALS["O"]

    def update_turn_count(self):
        """Update the turn count for this instance via updating self.turn_count"""

        self.turn_count += 1
        
    def update_turn(self):
        """Update whose turn it is via updating self.turn"""

        if self.turn == GAME_VALS["X"]:
            self.turn = GAME_VALS["O"]
        else:
            self.turn = GAME_VALS["X"]
    
    def get_turn(self):
        """
        Getter for self.turn.
        
        Returns:
            self.turn (integer): 1 for X's turn, -1 for O's turn.
        """

        return self.turn
    
    def get_turn_count(self):
        """
        Getter for self.turn_count, number of turns played
        
        Returns:
            self.turn_count (integer): Number of turns played
        """

        return self.turn_count
        
    def computer_check_for_win(self, game_board, score_move=False):
        """
        Function checks if the backtracking algorithm minimax produced a win, which is based on all possible move sets being run
        
        Args:
            game_board (dict): The game board to check if there is a win
            score_move (boolean) : True if desire to score themove
            
        Returns:
            True (boolean): A win
            False (boolean): A loss
            score (tuple) : If asking for a score, returns a tuple with first value being maximizer score (X), second being minimzer score (O)
        """

        diag_check = set()
        anti_diag_check = set()
        
        if score_move:
            max_depth_score = [0, 0]
        
        for rows in range(self.game_size):
            rows_check = set()
            col_check = set()
            for cols in range(self.game_size):
                rows_check.add(game_board[rows, cols])
                col_check.add(game_board[cols, rows])
            
            if self.find_a_winner([rows_check, col_check]):
                return True
            
            if score_move:
                maximizer_score, minimizer_score = self.score_the_move([rows_check, col_check])
                max_depth_score[0] += maximizer_score
                max_depth_score[1] += minimizer_score

            diag_check.add(game_board[rows, rows])
            anti_diag_check.add(game_board[rows, self.game_size-rows-1])
        
        if self.find_a_winner([diag_check, anti_diag_check]):
            return True
        
        if score_move:
                maximizer_score, minimizer_score = self.score_the_move([diag_check, anti_diag_check])
                max_depth_score[0] += maximizer_score
                max_depth_score[1] += minimizer_score
                
                return tuple(max_depth_score)
  
        return False
    
    def score_the_move(self, score_checks):
        """
        Finds a score by looking at all the rows, columns, and diagonals. If any contain one value and empty, assign a point
        if it was X (maximizer), and a negative point if it was for O (minimizer).
        
        Args:
            score_checks (list) : A list of sets
                These sets contain all unique values for the associated row/column/diagonal
        
        Return:
            score (tuple) : Tuple containing max score for X, and min score for O
        """

        score = [0, 0]
        for checks in score_checks:
            if len(checks) == 2:
                if GAME_VALS['EMPTY'] in checks:
                    if GAME_VALS['X'] in checks:
                        score[0] += 2
                    else:
                        score[1] += -2
        
        return tuple(score)
    
    def player_check_for_win(self, coordinates):
        """
        Checks if one of the player's won! Reads in the current instance's gameboard.
        Only checks for diagonal win if coordinates chosen lie on a diagonal.
        Only checks for win after first player has made 3 possible moves

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
            rows_check = set()
            col_check = set()
            diag_check = set()
            anti_diag_check = set()

            row = coordinates[0]
            col = coordinates[1]
            
            is_diagonal = self.check_if_diagonal(row, col)
            
            if is_diagonal:
                winning_checks = [rows_check, col_check, diag_check, anti_diag_check]
            else:
                winning_checks = [rows_check, col_check]
            
            for vals in range(self.game_size):
                rows_check.add(self.game_data[(row, vals)])
                col_check.add(self.game_data[(vals, col)])
                
                if is_diagonal:
                    diag_check.add(self.game_data[(vals, vals)])
                    anti_diag_check.add(self.game_data[(vals, self.game_size-vals-1)])
                    
            return self.find_a_winner(winning_checks)
               
    def check_if_diagonal(self, row, col):
        """
        Checks if the coordinate user chose lie on a diagonal

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
       
    def random_move_supplier(self):
        """
        Provides a random set of coordinates for the computer to choose 
        
        Return:
            (tuple): Coordinates that are currently unoccupied
        """

        self.empty_spots = [coords for coords, vals in self.game_data.items() if vals == GAME_VALS["EMPTY"]]
        
        return random.choice(self.empty_spots)

    def find_a_winner(self, winner_checks):
        """
        Finds a winner from a set of given checks, checks being the values listed in a row, column, diagonal, or anti-diagonal
        from the game board.
        
        Args:
            winner_checks (list) : A list of sets
                These sets contain all unique values for the associated row/column/diagonal
                If a single set contains only one unique non-empty value (i.e. 1 or -1), then someone has won
        
        Return:
            True (boolean) : There was a winner
            False (boolean) : There was no winner
        """

        for checks in winner_checks:
            if len(checks) == 1:
                if GAME_VALS['EMPTY'] not in checks:
                    return True
        
        return False
    
    def find_next_move_for_computer(self):
        """Function runs each possible move available through MINIMAX algorithm to determine a score for the next move.

        Returns:
            (tuple): Coordinates of best available next move
        """
        if self.game_size == 4:
            if self.turn_count <= 3:
                return self.random_move_supplier()
        elif self.game_size > 4:
            if self.turn_count <= (self.game_size):
                return self.random_move_supplier()
        
        available_moves = [coordinates for coordinates, value in self.game_data.items() if value == GAME_VALS["EMPTY"]]
        
        self.minimax_count = 0
        
        alpha = -1000000
        beta = 1000000
        
        self.possible_final_moves = {}
        gameboard_for_next_move = self.game_data
        for moves in available_moves:
            gameboard_for_next_move[moves] = self.turn
            # _ is returned turn count from minimax, and is ignored
            score_for_this_turn, _ = self.minimax_score_this_turn(self.turn * -1, gameboard_for_next_move, 0, alpha, beta)
            self.possible_final_moves[moves] = score_for_this_turn
            gameboard_for_next_move[moves] = GAME_VALS["EMPTY"]
            
        print(f"It took {self.minimax_count} iterations to get a move.")
                
        return self.find_best_turn(self.possible_final_moves)

    def minimax_score_this_turn(self, whose_turn, game_board, turn_count, alpha, beta):
        """
        Implements minimax algorithm, reads in a TicTacToe gameboard, performs algorithm to find potential best move
        This involves determining whether best move is offensive or defensive
        It creates a 'game tree', with each branch being a different possible game option
        It scores each tree based on its final state, per the score key below
        Scores assigned for gameboard positions:
        
        -10 for O win
        10 for X win
        Add # of turns to O score
        Subtract # of turns to X score
        
        Args:
            whose_turn (int): -1 for O's turn, 1 for X's turn
            game_board (dict): Keys = coordinates of spots, vals are -1 if O spot, 0 if EMPTY, 1 if X spot
            turn_count (int): Initialized at 0, counts the # of turns needed for a win in order to find optimal move
            alpha (int): Begins at negative infinity, starts low and is used as comparison in max evaluation
            beta (int): Begings at positive infinity, starts high and is used as comparison in min evaluation
        """

        self.minimax_count += 1
        
        if whose_turn == GAME_VALS["X"]:
            best = float('-inf')
        else:
            best = float('inf')
        
        if self.computer_check_for_win(game_board):
            if whose_turn == GAME_VALS["X"]:
                return -10, turn_count
            else:
                return 10, turn_count

        if turn_count > self.max_minimax_depth:
            # Insert heuristic here to give some points depending on situation of the board
            max_depth_score = self.computer_check_for_win(game_board, True)
            if whose_turn == GAME_VALS["X"]:
                return max_depth_score[0], turn_count
            else:
                return max_depth_score[1], turn_count
            
        if not self.check_spots_available(game_board):
            return 0, turn_count
                
        available_spaces = [coords for coords, vals in game_board.items() if vals == 0]
        scores = {}
        turns = {}
        for space in available_spaces:
            game_board[space] = whose_turn
            final_score, final_turn_count = self.minimax_score_this_turn(whose_turn * -1, game_board, turn_count + 1, alpha, beta)

            scores[space] = final_score
            turns[space] = final_turn_count
            game_board[space] = 0
            
            if whose_turn == GAME_VALS['X']:
                best = max(best, final_score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            else:
                best = min(best, final_score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            
        if whose_turn == GAME_VALS["O"]:
            return min(scores.values()) + min(turns.values()), min(turns.values())
        else:
            return max(scores.values()) - min(turns.values()), min(turns.values())

    def find_best_turn(self, next_moves):
        """
        Given a list of best possible turns, find the best possible turn in the shortest amount of turn. 
        Since move count is included in the score, this will just need to maximize score for X, and minimize for O.
        If multiple turns have the same score, it randomly chooses one.

        Args:
            next_moves (dict): Keys are next available moves, values are the score for that move

        Returns:
            (tuple): Coordinates of best possible move
        """
        
        if self.turn == GAME_VALS['X']:
            final_score = max([score for score in next_moves.values()])
        else:
            final_score = min([score for score in next_moves.values()])
            
        final_moves = [coords for coords, score in next_moves.items() if score == final_score]
        
        if len(final_moves) == 1:
            return final_moves[0]
        
        else:
            return random.choice(final_moves)
        
    def _display_game_board(self, game_size, game_board):
        print()
        for rows in range(game_size):
            for cols in range(game_size):
                value = [turn for turn, val in GAME_VALS.items() if val == game_board[(rows, cols)]]
                if value == ['EMPTY']:
                    value = [""]
                print(value, end=" ")
            print("")
        coordinates = [coords for coords, values in game_board.items()]

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeWindow(root)  
    root.mainloop()
