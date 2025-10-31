import arcade
import utils
from classes.tile import Tile
from utils import LEFT_BOUND, RIGHT_BOUND


class Collection:
    def __init__(self, tile=None): #assuming a collection will be created whenever a tile is added to the board alone
        self.tiles = [tile]
        self.isSet = True
        self.left_bound = LEFT_BOUND
        self.right_bound = RIGHT_BOUND
        if tile is not None:
            for tile in self.tiles:
                if tile.center_x < LEFT_BOUND and tile.center_x < self.left_bound:
                    self.left_bound = tile.center_x
                elif tile.center_x > RIGHT_BOUND and tile.center_x > self.right_bound:
                    self.right_bound = tile.center_x

    def add(self, tile, index):
        self.tiles.append(tile) #ensuring the list will be in the same order as on the board
                                       #could use positions to determine order if we want to make Tile less abstract?
        if tile.center_x < LEFT_BOUND and tile.center_x < self.left_bound:
            self.left_bound = tile.center_x
        elif tile.center_x > RIGHT_BOUND and tile.center_x > self.right_bound:
            self.right_bound = tile.center_x

    def remove(self, item):
        self.tiles.remove(item)
        if len(self.tiles) > 0:
            for tile in self.tiles:
                if tile.center_x < LEFT_BOUND and tile.center_x < self.left_bound:
                    self.left_bound = tile.center_x
                elif tile.center_x > RIGHT_BOUND and tile.center_x > self.right_bound:
                    self.right_bound = tile.center_x

    def clear(self):
        for e in self.tiles:
            self.tiles.remove(e)

    def get_tiles(self):
        return self.tiles


    def get_bounds(self):
        return self.left_bound, self.right_bound

    def get_length(self):
        return len(self.tiles)

    def getValue(self):
        sum = 0
        for tile in self.tiles:
            sum += tile.number
        return sum

    def set(self): #3-4 same number, different colors
        self.isSet = True
        if len(self.tiles) == 3:
            if self.tiles[0].color == self.tiles[1].color or self.tiles[0].color == self.tiles[2].color or self.tiles[1].color == self.tiles[2].color:
                return False
        elif len(self.tiles) == 4:
            if self.tiles[0].color == self.tiles[1].color or self.tiles[0].color == self.tiles[2].color or self.tiles[0].color == self.tiles[3].color\
                    or self.tiles[1].color == self.tiles[2].color or self.tiles[1].color == self.tiles[3].color or self.tiles[2].color == self.tiles[3].color:
                return False
        else: #incorrect length for set
            return False
        for tile in self.tiles:
            if tile.number != self.tiles[0].number:
                return False
        return self.isSet

    def run(self): #3+ same color, increasing numbers
        if len(self.tiles) < 3:
            return False
        for index in range(len(self.tiles)):
            if self.tiles[index].color != self.tiles[0].color:
                return False
            if index > 0 and not self.tiles[index - 1].number < self.tiles[index].number:
                return False
        return True

    def isValid(self):
        if self.set() == True or self.run() == True:
            return True
        return False