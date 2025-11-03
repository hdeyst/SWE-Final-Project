"""File containing collection class which holds logic for checking validity of sets and runs"""

class Collection:
    def __init__(self):
        self.tiles = []
        self.is_set = True

    def add(self, tile):
        self.tiles.append(tile)

    def remove(self, item):
        self.tiles.remove(item)

    def get_value(self):
        total = 0
        for tile in self.tiles:
            total += tile.number
        return total
    def clear(self):
        self.tiles.clear()

    def set(self): #3-4 same number, different colors
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
        for tile in self.tiles:
            if tile.number != self.tiles[0].number:
                return False
        return self.is_set

    def run(self): #3+ same color, increasing numbers
        if len(self.tiles) < 3:
            return False
        for index, name in enumerate(self.tiles):
            if name.color != self.tiles[0].color:
                return False
            if index > 0 and not self.tiles[index - 1].number < name.number:
                return False
        return True

    def is_valid(self):
        if self.set() or self.run():
            return True
        return False
