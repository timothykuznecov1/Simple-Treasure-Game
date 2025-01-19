import tkinter as tk
import random

# Game settings
GRID_SIZE = 5
NUM_TREASURES = 3
NUM_TRAPS = 2

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Game")
        self.grid_size = GRID_SIZE
        self.num_treasures = NUM_TREASURES
        self.num_traps = NUM_TRAPS
        self.treasures_collected = 0

        # Initialize the game board
        self.board, self.exit_pos = self.create_board()
        self.player_pos = (0, 0)

        # Create the UI
        self.create_ui()

    def create_board(self):
        board = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        empty_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        random.shuffle(empty_positions)

        # Place treasures
        for _ in range(self.num_treasures):
            x, y = empty_positions.pop()
            board[x][y] = "T"

        # Place traps
        for _ in range(self.num_traps):
            x, y = empty_positions.pop()
            board[x][y] = "X"

        # Place exit
        x, y = empty_positions.pop()
        board[x][y] = "E"

        return board, (x, y)

    def create_ui(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        # Display the status
        self.status_label = tk.Label(self.master, text="Treasures Collected: 0")
        self.status_label.pack()

        # Bind key events
        self.master.bind("<Up>", lambda event: self.move_player("up"))
        self.master.bind("<Down>", lambda event: self.move_player("down"))
        self.master.bind("<Left>", lambda event: self.move_player("left"))
        self.master.bind("<Right>", lambda event: self.move_player("right"))

        # Draw the initial board
        self.draw_board()

    def draw_board(self):
        cell_size = 400 // self.grid_size
        self.canvas.delete("all")

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = self.board[x][y]
                color = "white"

                if (x, y) == self.player_pos:
                    color = "yellow"  # Player
                elif cell == "T":
                    color = "green"  # Treasure
                elif cell == "X":
                    color = "red"  # Trap
                elif cell == "E":
                    color = "blue"  # Exit

                self.canvas.create_rectangle(
                    y * cell_size,
                    x * cell_size,
                    (y + 1) * cell_size,
                    (x + 1) * cell_size,
                    fill=color,
                    outline="black",
                )

    def move_player(self, direction):
        x, y = self.player_pos
        if direction == "up" and x > 0:
            x -= 1
        elif direction == "down" and x < self.grid_size - 1:
            x += 1
        elif direction == "left" and y > 0:
            y -= 1
        elif direction == "right" and y < self.grid_size - 1:
            y += 1
        else:
            return  # Invalid move

        new_pos = (x, y)
        self.player_pos = new_pos

        # Check the cell content
        cell = self.board[x][y]
        if cell == "T":
            self.treasures_collected += 1
            self.board[x][y] = "."  # Remove the treasure
            self.status_label.config(text=f"Treasures Collected: {self.treasures_collected}")
        elif cell == "X":
            self.status_label.config(text="You stepped on a trap! Game Over!")
            self.master.unbind("<Up>")
            self.master.unbind("<Down>")
            self.master.unbind("<Left>")
            self.master.unbind("<Right>")
        elif cell == "E":
            if self.treasures_collected == self.num_treasures:
                self.status_label.config(text="You Win! All treasures collected!")
            else:
                self.status_label.config(text="Collect all treasures before exiting!")

        # Redraw the board
        self.draw_board()


# Run the game
root = tk.Tk()
game = MazeGame(root)
root.mainloop()
