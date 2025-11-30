"""File containing the constants used throughout the project
    as well as any functions that aren't part of a class"""
import arcade
from arcade.examples.sound_demo import BUTTON_X_POSITIONS

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
NUM_TILES = 106

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
    },
    "ai_dock": {
        "occupied": arcade.color.TRANSPARENT_BLACK,
        "empty": arcade.color.TRANSPARENT_BLACK
    }
}
PLACEMENTS = ["grid", "dock", "ai_dock", "deck"]

# --- Gameplay constants ---
STARTING_TILE_AMT = 14
NUM_AI_PLAYERS = 1
TURN_TIME = 30


# --- Collection Bounds ---
LEFT_BOUND = 0
RIGHT_BOUND = 100000

TAB = " " * 4
# --- Instruction Values ---
INSTRUCTIONS = [f"Goal: be the first player to play all the tiles from your rack by forming them into sets",

                f"Placing tiles: ",
                f"{TAB} - Each tile is worth its face value (the number shown on the tile). ",
                f"{TAB}{TAB} - There are two jokers in the game. Each joker can be used as any tile in a set, and its "
                    f"number and color are that of the tile needed to complete the set",
                f"{TAB} - On turns after a player has made their initial meld, that player can build onto other sets "
                f"on the table with tiles from their rack.",
                f"{TAB} - When players cannot play any tiles from their racks, or choose not to, they must draw a tile."
                    f" After they draw, their turn is over.",

                f"{TAB} - Initial meld: ",
                f"{TAB}{TAB} - For their initial meld, players may not use tiles already played on the table",
                f"{TAB}{TAB} - In order to make an initial meld, each player must place tiles on the table in one or "
                    f"more sets that total at least 30 points.",
                f"{TAB}{TAB} - A joker used in the initial meld scores the value of the tile it represents.",
                f"{TAB}",

                f"Manipulation",
                f"{TAB} - Add one or more tiles from rack to make new set",
                f"{TAB} - Remove a fourth tile from a group and use it to form a new set",
                f"{TAB} - Add a fourth tile to a set and remove one tile from it, to make another set",
                f"{TAB} - Split an available set into two sets, and add tiles from rack to validate them",
                f"{TAB} - Each player has 30 seconds to make their turn",
                f"{TAB} ",

                f"Sets: ",
                f"{TAB} - A group is a set of either three or four tiles of the same number in different colors.",
                f"{TAB} - A run is a set of three or more consecutive numbers all in the same color.",
                f"{TAB} - The number 1 is always played as the lowest number, it cannot follow the number 13.",
                ]
INSTR_WIDTH = WINDOW_WIDTH - OUTER_MARGIN
INSTR_HEIGHT = WINDOW_HEIGHT - OUTER_MARGIN

KEY_BINDINGS = {
    "H": "Help screen",
    "K": "Show hotkeys",
    "L": "Lose screen",
    "W": "Win screen"
}

# --- Cheatsheet Variables ---
CHEATSHEET_BOTTOM = DOCK_OFFSET + 20
CHEATSHEET_WIDTH = 500
CHEATSHEET_HEIGHT = 25
MINIMIZED_CS_WIDTH = 160


# --- AI Dock Variables ---
AI_DOCK_YPOS = WINDOW_HEIGHT - GRID_HEIGHT - OUTER_MARGIN *2
AI_DOCK_XPOS = WINDOW_WIDTH - 23


PASS_BUTTON_POS = [WINDOW_WIDTH - OUTER_MARGIN * 2 - INNER_MARGIN * 2, TILE_HEIGHT * 2.7]

BUTTON_X = WINDOW_WIDTH - OUTER_MARGIN * 2 - INNER_MARGIN * 2
BUTTON_Y = TILE_HEIGHT * 2.8

END_TURN_BUTTON_POS = [WINDOW_WIDTH - OUTER_MARGIN * 2 - INNER_MARGIN * 2, TILE_HEIGHT]


""" ================== Helper functions ================== """

# --- Coordinate Converter ---
def convert_to_grid_coords(x, y):
    # Convert the clicked mouse position into grid coordinates
    column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
    row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

    return column, row

# --- Instructions Screen ---
def draw_instructions_screen(self):
    background = arcade.XYWH(self.center_x, self.center_y, INSTR_WIDTH, INSTR_HEIGHT)

    # color is "MIDNIGHT_GREEN" but the fourth value is transparency
    arcade.draw_rect_filled(rect=background, color=(0, 73, 83, 220))
    arcade.draw_rect_outline(rect=background, color=arcade.color.WHITE, border_width=2)

    title_ = arcade.Text("How to play Rummikub!",
                         self.center_x - 140, WINDOW_HEIGHT - 60,
                         color=arcade.color.WHITE, font_size=20)
    title_.draw()

    start_y = WINDOW_HEIGHT - 90
    start_x = OUTER_MARGIN
    for i, line in enumerate(INSTRUCTIONS):
        txt = arcade.Text(line, start_x, start_y, color=arcade.color.WHITE)
        txt.draw()
        start_y -= 30

    note = "For the official instructions, visit: https://rummikub.com/wp-content/uploads/2019/12/2600-English-1.pdf"
    ps = arcade.Text(note, start_x, 35, color=arcade.color.WHITE, font_size=10)
    ps.draw()