"""File containing the constants used throughout the project
    as well as any functions that aren't part of a class"""
import arcade

# --- Tile constants ---
TILE_SCALE = .265
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE
COLORS = {
    "cyan": arcade.color.CYAN,
    "red": arcade.color.RED,
    "yellow": arcade.color.YELLOW,
    "black": arcade.color.BLACK,
}
NUM_TILE_VALUES = 13

# --- Board Constants ---
INNER_MARGIN = 5
OUTER_MARGIN = 50
DECK_HEIGHT = 75

COLUMN_COUNT = 31
ROW_COUNT = 10

COLUMN_COUNT_DOCK = 27
ROW_COUNT_DOCK = 2

DOCK_LENGTH = COLUMN_COUNT_DOCK * (TILE_WIDTH + INNER_MARGIN)
OUTER_MARGIN_DOCK = ((TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT +
                     OUTER_MARGIN * 2) / 2 - DOCK_LENGTH / 2

DOCK_OFFSET = 3 * TILE_HEIGHT

# --- Screen constants ---
WINDOW_WIDTH = (TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT + OUTER_MARGIN * 2
WINDOW_HEIGHT = ((TILE_HEIGHT + INNER_MARGIN) * ROW_COUNT) + OUTER_MARGIN * 2 + DOCK_OFFSET
WINDOW_TITLE = "Rummikub Game Board!"

# --- Grid Variables ---
GRID_WIDTH = WINDOW_WIDTH * TILE_SCALE
GRID_HEIGHT = WINDOW_HEIGHT * TILE_SCALE

# --- Peg Variables ---
PEG_COLORS = {
    "grid": {
        "occupied": arcade.color.LAVENDER_BLUE,
        "empty": arcade.color.CEIL
    },
    "dock": {
        "occupied": arcade.color.PALE_COPPER,
        "empty": arcade.color.COPPER
    }
}
PLACEMENTS = ["grid", "dock"]

# --- Gameplay constants ---
STARTING_TILE_AMT = 14
NUM_PLAYERS = 1


# --- Collection Bounds ---
LEFT_BOUND = 0
RIGHT_BOUND = 100000

# --- Instruction Values ---
INSTRUCTIONS = ["INSTRUCTIONS",
                "Goal: ",
                "\tTo be the first player to play all the tiles from your rack by forming them into sets",
                "Sets: ",
                "\tA group is a set of either three or four tiles of the same number in different colors.",
                "\tA run is a set of three or more consecutive numbers all in the same color.",
                "\tThe number 1 is always played as the lowest number, it cannot follow the number 13.",
                "Placing tiles: ...",
                "Passing: ..."]

KEY_BINDINGS = {
    "D": "Draw tile",
    "S": "Save turn",
    "H": "Help screen",
    "K": "Show hotkeys",
    "L": "Lose screen",
    "Q": "Check moves",
    "U": "Undo changes",
    "W": "Win screen"
}

# --- Cheatsheet Variables ---
CHEATSHEET_BOTTOM = DOCK_OFFSET + 20
CHEATSHEET_WIDTH = WINDOW_WIDTH - OUTER_MARGIN * 2 + INNER_MARGIN
CHEATSHEET_HEIGHT = 25
MINIMIZED_CS_WIDTH = 160


""" ================== Helper functions ================== """

# --- Coordinate Converter ---
def convert_to_grid_coords(x, y):
    # Convert the clicked mouse position into grid coordinates
    column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
    row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

    return column, row

# --- Instructions Screen ---
def draw_instructions_screen(self):
    background = arcade.XYWH(self.center_x, self.center_y, 700, 400)

    # color is "MIDNIGHT_GREEN" but the fourth value is transparency
    arcade.draw_rect_filled(rect=background, color=(0, 73, 83, 220))
    arcade.draw_rect_outline(rect=background, color=arcade.color.WHITE, border_width=2)

    start_y = self.center_y + 200
    for i, line in enumerate(INSTRUCTIONS):
        start_y -= 30
        txt = arcade.Text(line, self.center_x - 320, start_y, color=arcade.color.WHITE)
        txt.draw()
