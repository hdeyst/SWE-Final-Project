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
                self.color = peg_colors["grid"]["occupied"]
                print(f"{self.placement} peg occupied!")
            else:
                self.color = peg_colors["dock"]["occupied"]
                print(f"{self.placement} peg occupied!")


    def empty_peg(self):
        self.tile = None
        if self.placement == "grid":
            self.color = peg_colors["grid"]["empty"]
        else:
            self.color = peg_colors["dock"]["empty"]

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