import arcade
from utils import *

peg_colors = {
    "grid": {
        "occupied": arcade.color.LAVENDER_BLUE,
        "empty": arcade.color.CEIL
    },
    "dock": {
        "occupied": arcade.color.PALE_COPPER,
        "empty": arcade.color.COPPER
    }
}

placements = ["grid", "dock"]

class Peg(arcade.SpriteSolidColor):

    def __init__(self, width, height, placement):
        super().__init__(width, height, color=peg_colors[placement]["empty"])

        # field for if a peg has a tile, should also work for checking if occupied
        self.Tile = None

        # peg must be either on grid or on dock
        self.placement = placement

    def is_occupied(self):
        if self.Tile is None:
            return False
        else:
            return True

    def get_tile(self):
        if self.Tile:
            return self.Tile
        else:
            return None

    def occupy_peg(self, tile):
        if not self.is_occupied():
            self.Tile = tile

            if self.placement == "grid":
                self.color = peg_colors["grid"]["occupied"]
            else:
                self.color = peg_colors["dock"]["occupied"]


    def empty_peg(self):
        self.Tile = None
        if self.placement == "grid":
            self.color = peg_colors["grid"]["empty"]
        else:
            self.color = peg_colors["dock"]["empty"]

    def set_center(self, x, y):
        self.center_x = x
        self.center_y = y
