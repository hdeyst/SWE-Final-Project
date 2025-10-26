"""
Defines 5 different types: Peg, Tile, Grid, and Dock
- Pegs are sprites representing the positions that a tile
  can be on the grid
- Tiles have color and value fields, represent game pieces
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
"""
import arcade.color
import math
from utils import *

class Peg(arcade.SpriteSolidColor):
    """A single peg sprite."""
    def __init__(self, width, height, color):
        super().__init__(width, height, color=color)

        # check if a tile is already on a given peg
        self.occupied = False
        # POSSIBLE field for if a peg has a tile
        self.Tile = None

        # determine if an individual peg is on the grid or in the dock
        # if we wanted to import Enum, we could but for now
        self.on_grid = False
        self.on_dock = False

    def toggle_occupied(self):
        # grid peg
        if self.on_grid:
            if self.occupied:
                self.occupied = False
                self.color = arcade.color.CEIL
            else:
                self.occupied = True
                self.color =arcade.color.LAVENDER_BLUE

        # dock peg
        if self.on_dock:
            if self.occupied:
                self.occupied = False
                self.color = arcade.color.COPPER
            else:
                self.occupied = True
                self.color = arcade.color.PALE_COPPER


class Grid():
    def __init__(self):
        # TODO: change these s.t. the grid is independent of the rest of the window
        # I want to be able to move the grid around in the space to make room
        # for the user dock and stuff
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
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.CEIL)

                peg.center_x = x
                peg.center_y = y

                peg.on_grid = True
                peg.on_dock = False

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

    # helper function
    def convert_to_grid_coords(self, x, y):
        # Convert the clicked mouse position into grid coordinates
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        return column, row

    def get_nearest_peg(self, tile):
        nearest_peg = arcade.get_closest_sprite(tile, self.peg_sprite_list)
        return nearest_peg[0]

class Dock():
    def __init__(self, board):
        self.board = board
        self.width = WINDOW_WIDTH

        for row in range(2):
            board.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = (row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN)

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.COPPER)

                peg.center_x = x
                peg.center_y = y
                peg.on_dock = True
                peg.on_grid = False

                board.peg_sprite_list.append(peg)
                board.peg_sprites[row].append(peg)

class Button():
    def __init__(self, width, height, color, x_pos, y_pos, text=''):
        self.width = width
        self.height = height
        self.color = color
        self.pressed_color = arcade.color.OLIVE
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.radius = self.height / 2
        self.pressed = False
    def draw(self):
        if self.pressed == False:
            arcade.draw_circle_filled(self.x_pos, self.y_pos, self.radius, self.color)
        else:
            arcade.draw_circle_filled(self.x_pos, self.y_pos, self.radius, self.pressed_color)
        arcade.draw_text(self.text, self.x_pos, self.y_pos, arcade.color.WHITE, 11,
                             anchor_x="center", anchor_y="center")

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x_pos)**2 + (pos[1] - self.y_pos)**2)
        return distance <= self.radius

    def set_color(self, color):
        self.color = color


