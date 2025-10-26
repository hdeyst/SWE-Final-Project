"""
Defines 2 different types: Grid, and Dock
- Pegs are sprites representing the positions that a tile
  can be on the grid
- Tiles have color and value fields, represent game pieces
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
"""
import arcade.color
from utils import *
from classes.peg import *

class Grid:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = DOCK_OFFSET + (row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN)

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, placement="grid")
                peg.set_center(x, y)

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

        print("peg_sprite_list: ")
        print([peg.position for peg in self.peg_sprite_list])
        print([convert_to_grid_coords(peg.center_x, peg.center_y) for peg in self.peg_sprite_list])


    def get_nearest_peg(self, tile):
        nearest_peg = arcade.get_closest_sprite(tile, self.peg_sprite_list)
        return nearest_peg[0]

class Dock(Grid):
    def __init__(self):
        super().__init__()
        # self.board = board
        self.width = WINDOW_WIDTH
        # self.height = WINDOW_HEIGHT

        # self.peg_sprites

        for row in range(2):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = (row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN)

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, placement="dock")

                peg.set_center(x, y)

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

