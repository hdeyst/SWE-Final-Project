import arcade
from utils import *

class Peg2(arcade.SpriteSolidColor):
    def __init__(self, width, height, placement, row, column):
        super().__init__(width, height, color=PEG_COLORS[placement]["empty"])

        # field for if a peg has a tile, should also work for checking if occupied
        self.tile = None
        # peg must be either on grid or on dock
        self.placement = placement

        # xy positions of peg
        self.row = row
        self.column = column

    def __str__(self):
        return (f"{self.placement} peg! "
                f"coords: {self.row}, {self.column} "
                f"tile: {self.tile}")

