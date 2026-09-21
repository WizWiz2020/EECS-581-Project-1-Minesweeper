"""
Tkinter UI for Minesweeper.

This module only knows how to draw a board and forward clicks — it has no
knowledge of mines, adjacency, or win/loss rules. main.py wires it to
minesweeper.py.
"""

import tkinter as tk

BOARD_SIZE = 10
TILE_SIZE = 40


class MinesweeperUI:
    def __init__(self, on_left_click, on_right_click):
        """
        on_left_click / on_right_click: callables of the form fn(row, col),
        invoked whenever a tile is clicked.
        """
        self.root = tk.Tk()
        self.root.title("EECS 581 - Minesweeper - Group 24")

        self.mine_image = self._load_scaled_image("mine.png", TILE_SIZE)
        self.flag_image = self._load_scaled_image("flag.png", TILE_SIZE)

        self.status_bar = tk.Frame(self.root)
        self.status_bar.pack(padx=10, pady=(10, 0), fill="x")

        self.mine_count_var = tk.StringVar(value="Mines: 0")
        tk.Label(
            self.status_bar,
            textvariable=self.mine_count_var,
            font=("TkDefaultFont", 11, "bold")
        ).pack(side="left")

        self.score_var = tk.StringVar(value="Flags: 0/0")
        tk.Label(
            self.status_bar,
            textvariable=self.score_var,
            font=("TkDefaultFont", 11, "bold")
        ).pack(side="right")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.tiles = []
        self._build_board(on_left_click, on_right_click)

    def update_mine_count(self, count):
        """
        Update the mines-remaining readout (mines placed minus flags set).
        """
        self.mine_count_var.set(f"Mines: {count}")

    def update_score(self, flags_placed, total_mines):
        """
        Update the scoreboard: how many flags are down out of the total
        mine count.
        """
        self.score_var.set(f"Flags: {flags_placed}/{total_mines}")

    def _load_scaled_image(self, path, target_size):
        """
        Load a PhotoImage and resize it (integer zoom/subsample,
        nearest-neighbor) toward target_size in each dimension. This uses
        plain tkinter only — no Pillow dependency — so the scaling is
        blocky rather than smooth, and only hits exact multiples of the
        source size. If you want smooth, exact scaling, swap this for
        Pillow's Image.resize(...) with ImageTk.PhotoImage.
        """
        image = tk.PhotoImage(file=path)
        width = image.width()
        if width <= 0:
            return image
        if width < target_size:
            factor = max(1, target_size // width)
            image = image.zoom(factor, factor)
        elif width > target_size:
            factor = max(1, round(width / target_size))
            image = image.subsample(factor, factor)
        return image

    def _build_board(self, on_left_click, on_right_click):
        # Tk only treats a Button's width/height as pixels when it's
        # displaying an image; with text only, they're character counts.
        # Giving every tile a real image at all times (a transparent
        # placeholder when covered/uncovered) keeps sizing pixel-based and
        # consistent across all four tile states, without needing a
        # wrapper Frame.
        self.blank_image = tk.PhotoImage(width=TILE_SIZE, height=TILE_SIZE)

        for r in range(BOARD_SIZE):
            row_tiles = []
            for c in range(BOARD_SIZE):
                tile = tk.Button(
                    self.frame,
                    image=self.blank_image,
                    width=TILE_SIZE,
                    height=TILE_SIZE,
                    compound="center",
                    borderwidth=1,
                    relief="raised",
                    command=lambda row=r, col=c: on_left_click(row, col)
                )
                tile.bind(
                    "<Button-3>",
                    lambda event, row=r, col=c: on_right_click(row, col)
                )
                tile.grid(row=r, column=c, padx=1, pady=1)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def set_tile(self, row, col, tile_type, number=0):
        tile = self.tiles[row][col]

        if tile_type == "covered":
            tile.config(
                image=self.blank_image,
                text="",
                compound="center",
                relief="raised",
                bg="SystemButtonFace"
            )

        elif tile_type == "uncovered":
            tile.config(
                image=self.blank_image,
                text=str(number) if number else "",  # 0 renders blank, not "0"
                compound="center",
                relief="sunken",
                bg="lightgray"
            )

        elif tile_type == "flag":
            tile.config(image=self.flag_image, text="", compound="center", relief="raised")

        elif tile_type == "mine":
            tile.config(image=self.mine_image, text="", compound="center", relief="sunken")

    def render(self, grid):
        """
        Redraw every tile from the current Cell grid (minesweeper.grid).
        Safe to call with grid=None (before the first click) — the board
        just stays in its initial all-covered state.
        """
        if grid is None:
            return

        for row in grid:
            for cell in row:
                if cell.is_flagged:
                    self.set_tile(cell.y, cell.x, "flag")
                elif not cell.is_revealed:
                    self.set_tile(cell.y, cell.x, "covered")
                elif cell.is_mine:
                    self.set_tile(cell.y, cell.x, "mine")
                else:
                    self.set_tile(cell.y, cell.x, "uncovered", cell.adjacent_mines)

    def run(self):
        self.root.mainloop()
