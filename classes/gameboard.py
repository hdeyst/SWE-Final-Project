import arcade

import utils
from classes.gridboard import Grid, Dock
from utils import convert_to_grid_coords


class Gameboard:
    def __init__(self):
        self.grid = Grid()
        self.dock = Dock()

        # make a mega list of all pegs from dock and grid
        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)
        for dp in self.dock.peg_sprite_list:
            self.all_pegs.append(dp)

        # print out grid coors as well as technical screen coords
        for peg in self.all_pegs:
            print(f"{peg.position} : "
                  f"{convert_to_grid_coords(peg.center_x, peg.center_y)}")
