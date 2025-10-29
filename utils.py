import arcade
from arcade.examples.array_backed_grid_sprites_2 import COLUMN_COUNT
from arcade.future.input.input_manager_example import WINDOW_WIDTH

# --- Tile constants ---
TILE_SCALE = .3
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE
COLORS = {
    "cyan": arcade.color.CYAN,
    "red": arcade.color.RED,
    "yellow": arcade.color.YELLOW,
    "black": arcade.color.BLACK,
}

# --- Board Constants ---
INNER_MARGIN = 5
OUTER_MARGIN = 50
DECK_HEIGHT = 75

# --- Window constants ---
# WINDOW_WIDTH = 1280
# WINDOW_HEIGHT = 720
# WINDOW_TITLE = "Tile Example"

COLUMN_COUNT = 24
ROW_COUNT = 8

COLUMN_COUNT_DOCK = 24
ROW_COUNT_DOCK = 2

DOCK_LENGTH = COLUMN_COUNT_DOCK * (TILE_WIDTH + INNER_MARGIN)
OUTER_MARGIN_DOCK = ((TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT + OUTER_MARGIN * 2) / 2 - DOCK_LENGTH / 2
#OUTER_MARGIN_DOCK = (WINDOW_WIDTH - DOCK_LENGTH) / 2


DOCK_OFFSET = (3 * TILE_HEIGHT)
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


""" Helper functions """

# --- Coordinate Converter ---
def convert_to_grid_coords(x, y):
    # Convert the clicked mouse position into grid coordinates
    column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
    row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

    return column, row

# --- Gameplay constants ---
STARTING_TILE_AMT = 14