"""
Defines 2 different types: Grid, and Dock
- Pegs are sprites representing the positions that a tile
  can be on the grid
- Tiles have color and value fields, represent game pieces
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
"""
import arcade.color
import math
from ..utils import *
from peg import *

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

    def get_nearest_peg(self, tile):
        nearest_peg = arcade.get_closest_sprite(tile, self.peg_sprite_list)
        return nearest_peg[0]

    def draw(self):
        arcade.draw_rect_filled(
            arcade.LBWH(left=OUTER_MARGIN,
                        bottom=DOCK_OFFSET + OUTER_MARGIN,
                        width=COLUMN_COUNT * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                        height=ROW_COUNT * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN
                        ),
            color=arcade.color.SHADOW_BLUE
        )

class Dock(Grid):
    def __init__(self):
        super().__init__()
        # self.board = board
        self.width = WINDOW_WIDTH
        # self.height = WINDOW_HEIGHT

        # self.peg_sprites

        for row in range(ROW_COUNT_DOCK):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT_DOCK):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = (row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN)

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, placement="dock")

                peg.set_center(x, y)

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

    def draw(self):
        arcade.draw_rect_filled(
            arcade.LBWH(left=OUTER_MARGIN,
                        bottom=OUTER_MARGIN,
                        width=COLUMN_COUNT_DOCK * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                        height= ROW_COUNT_DOCK * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN),
            color=arcade.color.ROSY_BROWN
        )

class Button():
    def __init__(self, width, height, color, x_pos, y_pos, text=''):
        self.width = width
        self.height = height
        self.color = color
        self.pressed_color = arcade.color.TROPICAL_RAIN_FOREST
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
        button_text = arcade.Text(self.text, self.x_pos, self.y_pos, arcade.color.BLACK, 11,
                             anchor_x="center", anchor_y="center")
        button_text.draw()

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.x_pos)**2 + (pos[1] - self.y_pos)**2)
        return distance <= self.radius

    def set_color(self, color):
        self.color = color


