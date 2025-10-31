import arcade
import utils
from classes.tile import Tile
from utils import LEFT_BOUND, RIGHT_BOUND


class Collection:
    def __init__(self): #assuming a collection will be created whenever a tile is added to the board alone
        self.tiles = []

    def add(self, tile):
        self.tiles.append(tile)

    def remove(self, item):
        self.tiles.remove(item)
        if len(self.tiles) > 0:
            for tile in self.tiles:
                if tile.center_x < LEFT_BOUND and tile.center_x < self.left_bound:
                    self.left_bound = tile.center_x
                elif tile.center_x > RIGHT_BOUND and tile.center_x > self.right_bound:
                    self.right_bound = tile.center_x

    def clear(self):
        self.tiles.clear()

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
            if self.tiles[0].get_color() == self.tiles[1].get_color() or self.tiles[0].get_color() == self.tiles[2].get_color() or self.tiles[1].get_color() == self.tiles[2].get_color():
                return False
        elif len(self.tiles) == 4:
            if self.tiles[0].get_color() == self.tiles[1].get_color() or self.tiles[0].get_color() == self.tiles[2].get_color() or self.tiles[0].get_color() == self.tiles[3].get_color()\
                    or self.tiles[1].get_color() == self.tiles[2].get_color() or self.tiles[1].get_color() == self.tiles[3].get_color() or self.tiles[2].get_color() == self.tiles[3].get_color():
                return False
        else: #incorrect length for set
            return False
        for tile in self.tiles:
            if tile.get_number() != self.tiles[0].get_number():
                return False
        return True

    def run(self): #3+ same color, increasing numbers
        if len(self.tiles) < 3:
            return False
        for index in range(len(self.tiles)):
            if self.tiles[index].get_color() != self.tiles[0].get_color():
                return False
            if index > 0 and not self.tiles[index - 1].get_number() < self.tiles[index].get_number():
                return False
        return True

    def is_valid(self):
        if self.set() or self.run():
            return True
        return False