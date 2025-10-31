import arcade
from ..utils import *

class Peg(arcade.SpriteSolidColor):

    def __init__(self, width, height, placement):
        super().__init__(width, height, color=PEG_COLORS[placement]["empty"])

        # field for if a peg has a tile, should also work for checking if occupied
        self.tile = None

        # peg must be either on grid or on dock
        self.placement = placement

    def is_occupied(self):
        if self.tile is None:
            return False
        return True

    def get_tile(self):
        if self.tile:
            return self.tile
        return None

    def occupy_peg(self, tile):
        if not self.is_occupied():
            self.tile = tile

            if self.placement == "grid":
                self.color = PEG_COLORS["grid"]["occupied"]
            else:
                self.color = PEG_COLORS["dock"]["occupied"]


    def empty_peg(self):
        self.tile = None
        if self.placement == "grid":
            self.color = PEG_COLORS["grid"]["empty"]
        else:
            self.color = PEG_COLORS["dock"]["empty"]

    def set_center(self, x, y):
        self.center_x = x
        self.center_y = y

    def get_center(self):
        return self.center_x, self.center_y

    def get_grid_coords(self):
        return convert_to_grid_coords(self.center_x, self.center_y)

    def __str__(self):
        return (f"{self.placement} peg! "
                f"coords: {self.get_grid_coords()} "
                f"tile: {self.tile}")