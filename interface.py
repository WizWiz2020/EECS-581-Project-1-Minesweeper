import tkinter as tk

# Constants
BOARD_SIZE = 10
TILE_SIZE = 40

root = tk.Tk()
root.title("EECS 581 - Minesweeper - Group 24")

# Images
mineImage = tk.PhotoImage(file="mine.png")
flagImage = tk.PhotoImage(file="flag.png")

# Board
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Store all tiles so they can be changed later
tiles = []

# On Click functions

def on_left_click(row, col):
    #Stub
    print("Left click:", row, col)


def on_right_click(row, col):
    #Stub
    print("Right click:", row, col)


# Tile Functions

def set_tile(row, col, tile_type, number=0):

    tile = tiles[row][col]

    if tile_type == "covered":
        tile.config(
            image="",
            text="",
            relief="raised",
            bg="SystemButtonFace"
        )

    elif tile_type == "uncovered":
        tile.config(
            image="",
            text=str(number),
            relief="sunken",
            bg="lightgray"
        )

    elif tile_type == "flag":
        tile.config(
            image=flagImage,
            text="",
            relief="raised"
        )

    elif tile_type == "mine":
        tile.config(
            image=mineImage,
            text="",
            relief="sunken"
        )



# Board creation

for r in range(BOARD_SIZE):

    row_tiles = []

    for c in range(BOARD_SIZE):

        tile = tk.Button(
            frame,
            width=TILE_SIZE // 10,
            height=TILE_SIZE // 20,
            borderwidth=1,
            relief="raised"
        )

        # Left click
        tile.bind(
            "<Button-1>",
            lambda event, row=r, col=c:
                on_left_click(row, col)
        )

        # Right click
        tile.bind(
            "<Button-3>",
            lambda event, row=r, col=c:
                on_right_click(row, col)
        )

        tile.grid(
            row=r,
            column=c,
            padx=1,
            pady=1
        )

        row_tiles.append(tile)

    tiles.append(row_tiles)

root.mainloop()