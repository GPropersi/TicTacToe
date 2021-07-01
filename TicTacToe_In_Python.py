from time import time
from tkinter import messagebox

import tkinter as tk

"""
Play TicTacToe!
This script allows you to play any size grid of TicTacToe with another person, in the console.
Have fun!
"""

GAME_VALS = {
    'X': 'X',
    'EMPTY': '_',
    'O': 'O'
}

MAX_BOARD_SIZE = 10

class TicTacToeWindow:
    """Window to play TicTacToe on!
    """
    def __init__(self, root):
        self.root = root
        self.root.title("TicTacToe!")
        self.window = tk.Label(self.root, text="Play TicTacToe!", font=("Helvetica", 20))
        self.window.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        self.size_input_label = tk.Label(self.root, text="Enter the size of the board you want to play: ", font=("Helvetica", 10))
        self.size_input_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.size_input = tk.Entry(self.root)
        self.size_input.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        self.size_capture = tk.Button(self.root, width=25, text="Let's Play!", font=("Helvetica", 10), command=self.getSizeOfBoard)
        self.size_capture.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        
        
    def getSizeOfBoard(self):
        """Get the user to provide the size of the board they want to play. Max size = MAX_BOARD_SIZE
        Inputs: N/A
        Outputs: 
            sizeOfBoard (int) = Length of one side of the TicTacToe board they wish to play on
        """
        if not self.size_input.get().isdigit():
            messagebox.showerror("Error",f"Please enter a valid positive size, max size {MAX_BOARD_SIZE},\nand greater than 0.")
            return
        
        self.sizeOfBoard = self.size_input.get()
        try:
            if 0 < int(self.sizeOfBoard) <= MAX_BOARD_SIZE:
                # Number is positive and greater than zero, less than/inclusive of max board size.
                return int(self.sizeOfBoard)
            
            else:
                messagebox.showerror("Error",f"Please enter a valid positive size, max size {MAX_BOARD_SIZE},\nand greater than 0.")
                return
            
        except ValueError:
            messagebox.showerror("Error",f"Please enter a valid positive size, max size {MAX_BOARD_SIZE},\nand greater than 0.")
            return
                

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
    print(
    """
    You are playing TicTacToe!\n\
    The goal is to fill a row, column, or diagonal with only your pieces!.\n\
    If neither you nor your opponent can create a winning pattern, it's a cat's game!\n\
    Note, please consider top left corner to be postion 1 x 1.
    """)
    root = tk.Tk()
    TicTacToeWindow(root)
    
    root.mainloop()
    # main()