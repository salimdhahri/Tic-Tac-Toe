"""A tic-tac-toe game built with Python and Tkinter."""
# Sources used: https://realpython.com/tic-tac-toe-python/ - For creating the game that is initially player v player.

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Player:
    def __init__(self, label, color):
        self.label = label
        self.color = color

class ComputerPlayer(Player):
    def __init__(self, label, color):
        super().__init__(label, color)

    def process_move(self, game):
        print("Processing the move as a computer")
        move = self.find_best_move(game)
        return move

    def find_best_move(self, game):
        print("Finding the best move as a computer")
        best_score = float("-inf")
        best_move = None
        for row in range(game.board_size):
            print("Checking row: ", row)
            for col in range(game.board_size):
                print("Checking col: ", col)
                move = Move(row, col, self.label)
                if game.is_valid_move(move):
                    game.process_move(move) 
                    if game.gameDifficulty == 1:
                        score = self.dfs(game, 0, False)
                    elif game.gameDifficulty == 2:
                        score = self.minimax(game, 0, False, float("-inf"), float("inf"))
                    game.undo_move(move)
                    if score > best_score:
                        best_score = score
                        best_move = move
        print("Finished checking all the rows and columns")
        return best_move

    def dfs(self, game, depth, is_maximizing):
        # If the game has a winner, return a score based on who won
        if game.has_winner():
            if game.current_player.label == self.label:  # If the current player is the computer player
                return 1  # Return a score of 1
            else:
                return -1  # Return a score of -1
        # If the game is tied, return a score of 0
        elif game.is_tied():
            return 0
    
        if is_maximizing:
            # If it's the computer's turn, find the move with the highest score
            best_score = float("-inf")  # Initialize the best score to negative infinity
            for row in range(game.board_size):
                for col in range(game.board_size):
                    move = Move(row, col, self.label)  # Create a move for the computer player
                    if game.is_valid_move(move):
                        game.process_move(move)  # Process the move on a copy of the game board
                        score = self.dfs(game, depth + 1, False)  # Recursively call dfs for the next player (human)
                        game.undo_move(move)  # Undo the move to explore other possibilities
                        best_score = max(score, best_score)  # Update the best score
            return best_score  # Return the best score found
        else:
            # If it's the human player's turn, find the move with the lowest score
            best_score = float("inf")  # Initialize the best score to positive infinity
            for row in range(game.board_size):
                for col in range(game.board_size):
                    move = Move(row, col, game.current_player.label)  # Create a move for the human player
                    if game.is_valid_move(move):
                        game.process_move(move)  # Process the move on a copy of the game board
                        score = self.dfs(game, depth + 1, True)  # Recursively call dfs for the next player (computer)
                        game.undo_move(move)  # Undo the move to explore other possibilities
                        best_score = min(score, best_score)  # Update the best score
            return best_score  # Return the best score found

        
    def minimax(self, game, depth, is_maximizing, alpha, beta):
        if game.has_winner():
            if game.current_player.label == self.label:
                return 1  # If the computer player wins, return a score of 1
            else:
                return -1  # If the human player wins, return a score of -1
        elif game.is_tied():
            return 0  # If the game is tied, return a score of 0

        if is_maximizing:
            best_score = float("-inf")  # Initialize the best score to negative infinity
            for row in range(game.board_size):
                for col in range(game.board_size):
                    move = Move(row, col, self.label)
                    if game.is_valid_move(move):
                        game.process_move(move)
                        score = self.minimax(game, depth + 1, False, alpha, beta)
                        game.undo_move(move)
                        best_score = max(score, best_score)  # Update the best score
                        alpha = max(alpha, best_score)  # Update alpha for alpha-beta pruning
                        if beta <= alpha:
                            break  # Beta cutoff, no need to go further
            return best_score
        else:
            best_score = float("inf")  # Initialize the best score to positive infinity
            for row in range(game.board_size):
                for col in range(game.board_size):
                    move = Move(row, col, game.current_player.label)
                    if game.is_valid_move(move):
                        game.process_move(move)
                        score = self.minimax(game, depth + 1, True, alpha, beta)
                        game.undo_move(move)
                        best_score = min(score, best_score)  # Update the best score
                        beta = min(beta, best_score)  # Update beta for alpha-beta pruning
                        if beta <= alpha:
                            break  # Alpha cutoff, no need to go further
            return best_score
        
#The .row and .col attributes will hold the coordinates 
#that identify the move’s target cell.
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3


class TicTacToeGame:
    def __init__(self, gameDiff, players, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self.gameDifficulty = gameDiff
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()


    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        print("Processing a player's move")
        row, col = move.row, move.col # Gets the .row and .col coords from the input move
        self._current_moves[row][col] = move # Assigns the input move to the item at [row][col] in the list of current moves
        for combo in self._winning_combos: # Starts a loop over the winning combos
            results = set(self._current_moves[n][m].label for n, m in combo) # Runs a generator expression that retrieves all the labels from the moves in the current winning combos.
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
        print("Processing move has ended")

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        print("Checking if the game has a winner")
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        print("Checking if the game is tied")
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player."""
        print("Changing players")
        print("The current player is: ", self.current_player.label)
        self.current_player = next(self._players)
        print("The new player is: ", self.current_player.label)
        print("Is the new player a ComputerPlayer?", isinstance(self.current_player, ComputerPlayer))

    def reset_game(self):
        """Reset the game state to play again."""
        print("Restarting the game")
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []
    def undo_move(self, move):
        """Undo the given move."""
        print("Undoing the move...")
        row, col = move.row, move.col
        self._current_moves[row][col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = [] 


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self) #Creates a Frame object to hold the game’s grid of cells.
        grid_frame.pack() # Uses the .pack() geometry manager to place the frame object on the main window.
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50) # Configure the width and minimum size of every cell on the grid.
            self.columnconfigure(row, weight=1, minsize=75) # Configure the width and minimum size of every cell on the grid.
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")


    def play(self, event=None):
        """Handle a player's move."""
        if event is not None and isinstance(self._game.current_player, ComputerPlayer):
            # If it's the computer's turn, ignore the click event
            return

        if isinstance(self._game.current_player, ComputerPlayer):
            move = self._game.current_player.process_move(self._game)
            self._update_button(self._get_button(move))
        else:
            if event is None:
                return
            clicked_btn = event.widget
            row, col = self._cells[clicked_btn]
            move = Move(row, col, self._game.current_player.label)
            if not self._game.is_valid_move(move):
                return
            self._update_button(clicked_btn)

        self._game.process_move(move)
        if self._game.is_tied():
            self._update_display(msg="Tied game!", color="red")
        elif self._game.has_winner():
            self._highlight_cells()
            msg = f'Player "{self._game.current_player.label}" won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            if isinstance(self._game.current_player, ComputerPlayer):
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
                self.after(500, self.play)
            else:
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
    def _get_button(self, move):
        for button, coordinates in self._cells.items():
            if coordinates == (move.row, move.col):
                return button
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)


def main():
    """Create the game's board and run its main loop."""
    gameDiff = int(input("Enter difficulty (1 - 2)\n"))
    players = (
        Player(label="X", color="blue"),
        ComputerPlayer(label="O", color="green"),
    )
    game = TicTacToeGame(gameDiff, players)
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
