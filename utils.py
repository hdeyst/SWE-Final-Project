import arcade

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

COLUMN_COUNT = 20
ROW_COUNT = 7

DOCK_OFFSET = (3 * TILE_HEIGHT)
# --- Screen constants ---
WINDOW_WIDTH = (TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT + OUTER_MARGIN * 2
WINDOW_HEIGHT = ((TILE_HEIGHT + INNER_MARGIN) * ROW_COUNT) + OUTER_MARGIN * 2 + DOCK_OFFSET
WINDOW_TITLE = "Rummikub Game Board!"