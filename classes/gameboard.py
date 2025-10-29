import arcade
from classes.gridboard import Grid, Dock

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

        # print out grid coords
        for peg in self.all_pegs:
            print(peg)
