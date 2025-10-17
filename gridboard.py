"""
Defines 3 different types: Peg, Tile, and Grid
- Pegs are sprites representing the positions that a tile
  can be on the grid
- Tiles have color and value fields, represent game pieces
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
"""
from utils import *

class Peg(arcade.SpriteSolidColor):
    """A single peg sprite."""
    def __init__(self, width, height, color):
        super().__init__(width, height, color=color)

        # check if a tile is already on a given peg
        self.occupied = False
        # POSSIBLE field for if a peg has a tile
        self.Tile = None

class Tile(arcade.Sprite):
    """A single tile sprite."""
    def __init__(self, filename, color, value, scale=1):
        super().__init__(filename, scale)
        self.tile_color = color
        self.value = value


class Grid():
    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []


        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.CEIL)

                peg.center_x = x
                peg.center_y = y

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

    # helper function
    def convert_to_grid_coords(self, x, y):
        # Convert the clicked mouse position into grid coordinates
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        return column, row

    def get_nearest_peg(self, x, y):
        nearest_peg = arcade.get_sprites_at_point((x, y), self.peg_sprite_list)
        return nearest_peg[0]
