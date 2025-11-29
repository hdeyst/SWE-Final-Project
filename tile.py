"""a tile sprite which has a color, number, and reset/position functionality"""

import arcade
from utils import TILE_SCALE

class Tile(arcade.Sprite):
    """A single tile sprite."""
    color = ""
    number = 0
    wild = ""
    is_wild = False

    start_of_turn_x = 0
    start_of_turn_y = 0
    peg = None
    in_dock = True
    start_in_dock = True #for reset functionality
    placement = "deck"

    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        # tile = Tile(f"tiles/{color}_{j + 1}.png", utils.TILE_SCALE)
        split = filename.split("_")
        color_split = split[0].split("tiles/")
        self.color = color_split[1]
        number_split = split[1].split(".")
        try:
            self.number = int(number_split[0])
        except ValueError:
            self.color = color_split[1] + number_split[0]
            self.number = 0
            self.is_wild = True

    def __str__(self):
        return f"{self.color}{self.number}"

    #sets start of turn positions (x and y) to input
    def set_start_of_turn_pos(self, x, y):
        self.start_of_turn_x = x
        self.start_of_turn_y = y

    def set_number(self, number):
        self.number = number
