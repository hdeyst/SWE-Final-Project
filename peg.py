"""File holding Peg class"""
import arcade
from utils import PEG_COLORS, convert_to_grid_coords

class Peg(arcade.SpriteSolidColor):
    """Class for peg sprite and associated information like position and tile information."""
    def __init__(self, width, height, placement):
        super().__init__(width, height, color=PEG_COLORS[placement]["empty"])

        # field for if a peg has a tile, should also work for checking if occupied
        self.tile = None

        # peg must be either on grid or on dock
        self.placement = placement

    def is_occupied(self):
        """returns True if tile has a value"""
        if self.tile is None:
            return False
        return True

    def get_tile(self):
        """returns tile"""
        if self.tile:
            return self.tile
        return None

    def occupy_peg(self, tile):
        """sets tile field to input and changes peg color"""
        if not self.is_occupied():
            self.tile = tile

            if self.placement == "grid":
                self.color = PEG_COLORS["grid"]["occupied"]
            else:
                self.color = PEG_COLORS["dock"]["occupied"]


    def empty_peg(self):
        """sets tile field to none and changes peg color"""
        self.tile = None
        if self.placement == "grid":
            self.color = PEG_COLORS["grid"]["empty"]
        else:
            self.color = PEG_COLORS["dock"]["empty"]

    def set_center(self, x, y):
        """sets peg position"""
        self.center_x = x
        self.center_y = y

    def get_center(self):
        """returns peg position"""
        return self.center_x, self.center_y

    def get_grid_coords(self):
        """returns peg position in grid coordinate form"""
        return convert_to_grid_coords(self.center_x, self.center_y)

    def __str__(self):
        return (f"{self.placement} peg! "
                f"coords: {self.get_grid_coords()} "
                f"tile: {self.tile}")
