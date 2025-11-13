"""File holding Gameboard class"""
import arcade
from gridboard import Grid, Dock
from utils import (COLUMN_COUNT, COLUMN_COUNT_DOCK, ROW_COUNT, ROW_COUNT_DOCK,
                   WINDOW_WIDTH, WINDOW_HEIGHT)


class Gameboard:
    def __init__(self):
        self.grid = Grid("grid", COLUMN_COUNT, ROW_COUNT)
        self.dock = Dock("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)

        # make a mega list of all pegs from dock and grid
        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)
        for dp in self.dock.peg_sprite_list:
            self.all_pegs.append(dp)

        # create the logo
        self.texture = arcade.load_texture("./misc/rummikub.png", )
        self.logo_sprite = arcade.Sprite(self.texture, scale=.2)
        self.logo_sprite.center_y = WINDOW_HEIGHT - 25
        self.logo_sprite.center_x = WINDOW_WIDTH / 2

    def draw(self):
        self.grid.draw()
        self.dock.draw()

        arcade.draw_sprite(self.logo_sprite)


