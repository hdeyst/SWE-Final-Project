import arcade
from classes.gridboard import Grid, Dock
from utils import *

class Gameboard:
    def __init__(self):
        self.grid = Grid()
        self.dock = Dock()
        self.coords_dict = {}

        # make a mega list of all pegs from dock and grid
        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)
        for dp in self.dock.peg_sprite_list:
            self.all_pegs.append(dp)

        # add peg coordinates to a dictionary. keys are the grid coords, values are the window coords
        for peg in self.all_pegs:
            self.coords_dict[convert_to_grid_coords(peg.center_x, peg.center_y)] = peg.position

        # print out grid coords
        # for peg in self.all_pegs:
        #     print(peg)

        # for coord in self.coords_dict:
        #     print(f"{coord}: {self.coords_dict[coord]}")

    def draw(self):
        self.grid.draw()
        self.dock.draw()

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
