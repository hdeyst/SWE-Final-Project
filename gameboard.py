"""File holding Gameboard class"""
import arcade
from gridboard import Grid, Dock
from utils import (convert_to_grid_coords, COLUMN_COUNT, COLUMN_COUNT_DOCK, ROW_COUNT, ROW_COUNT_DOCK,
                   WINDOW_WIDTH, WINDOW_HEIGHT)


class Gameboard:
    def __init__(self):
        self.grid = Grid("grid", COLUMN_COUNT, ROW_COUNT)
        self.dock = Dock("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)
        self.coords_dict = {}

        # make a mega list of all pegs from dock and grid
        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)
        for dp in self.dock.peg_sprite_list:
            self.all_pegs.append(dp)

        # add peg coordinates to a dictionary. keys are the grid coords, values
        # are the window coords
        for peg in self.all_pegs:
            self.coords_dict[convert_to_grid_coords(peg.center_x, peg.center_y)] = peg.position

        # create the logo
        self.texture = arcade.load_texture("./misc/rummikub.png", )
        self.logo_sprite = arcade.Sprite(self.texture, scale=.2)
        self.logo_sprite.center_y = WINDOW_HEIGHT - 25
        self.logo_sprite.center_x = WINDOW_WIDTH / 2

    def draw(self):
        self.grid.draw()
        self.dock.draw()

        arcade.draw_sprite(self.logo_sprite)

    # use the coord dictionary to get peg neighbors
    def get_left_peg_neighbor(self, peg):
        x, y = convert_to_grid_coords(peg.center_x, peg.center_y)

        # no left neighbor if at index 0
        if x:
            x -= 1
            neighbor = self.coords_dict[(x, y)]
            pegs = arcade.get_sprites_at_point(neighbor, self.all_pegs)
            if pegs[-1]:
                return pegs[-1]
        return False

    # use the coord dictionary to get peg neighbors
    def get_right_peg_neighbor(self, peg):
        x, y = convert_to_grid_coords(peg.center_x, peg.center_y)

        # no right neighbor if at rightmost index
        if ((peg.placement == "dock" and x < COLUMN_COUNT_DOCK-1) or
                (peg.placement == "grid" and x < COLUMN_COUNT-1)):
            x += 1
            neighbor = self.coords_dict[(x, y)]
            pegs = arcade.get_sprites_at_point(neighbor, self.all_pegs)
            if pegs[-1]:
                return pegs[-1]
        return False
