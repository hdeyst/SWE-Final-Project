"""File containing collection class which holds logic for checking validity of sets and runs"""

class Collection:
    def __init__(self):
        self.tiles = []
        self.is_set = True
        self.contains_wild = False

    def add(self, tile):
        self.tiles.append(tile)
        self.has_wild()

    def remove(self, item):
        self.tiles.remove(item)
        self.has_wild()

    def has_wild(self):
        for tile in self.tiles:
            if tile.is_wild:
                self.contains_wild = True
        if self.contains_wild:
            return True
        return False

    def get_value(self):
        total = 0
        for tile in self.tiles:
            total += tile.number
        return total

    def clear(self):
        self.tiles.clear()

    def is_valid(self):
        if self.set() or self.run():
            return True
        return False

    def get_num_tiles(self):
        return len(self.tiles)

    def get_tiles(self):
        return self.tiles

    # 3-4 tiles of the same number, different colors
    def set(self):
        index = 0
        self.is_set = True
        if len(self.tiles) == 3:
            if (self.tiles[0].color == self.tiles[1].color or
                    self.tiles[0].color == self.tiles[2].color or
                    self.tiles[1].color == self.tiles[2].color):
                return False
        elif len(self.tiles) == 4:
            if (self.tiles[0].color in (self.tiles[1].color, self.tiles[2].color,
                                        self.tiles[3].color) or
                    self.tiles[1].color in (self.tiles[2].color, self.tiles[3].color) or
                    self.tiles == self.tiles[3].color):
                return False
        else: #incorrect length for set
            return False
        for i, tile in enumerate(self.tiles): #get index of the non-wild tile
            if tile.is_wild:
                pass
            else:
                index = i
        for tile in self.tiles: #check that all tiles have the same number
            if tile.number != self.tiles[index].number:
                if tile.is_wild:
                    pass
                else:
                    return False

        return self.is_set

    # 3+tiles of the same color, increasing numbers by 1
    def run(self):
        index = 0
        if len(self.tiles) < 3:
            return False

        for i, tile in enumerate(self.tiles): #get index of the non-wild tile
            if tile.is_wild:
                pass
            else:
                index = i

        for i, name in enumerate(self.tiles): # check that all tiles have the same color
            if name.color != self.tiles[index].color:
                if name.is_wild:
                    pass
                else:
                    return False
            if i > 0 and not self.tiles[i - 1].number + 1 == name.number:
                if name.is_wild or self.tiles[i - 1].is_wild:
                    pass
                else:
                    return False
        return True

    def __str__(self):
        rep = ""
        for tile in self.tiles:
            rep = rep + str(tile) + ", "
        return rep
