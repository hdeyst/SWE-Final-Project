"""File containing collection class which holds logic for checking validity of sets and runs"""

class Collection:
    def __init__(self):
        self.tiles = []
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

    def get_wild_index(self):
        wilds = []
        for i, tile in enumerate(self.tiles):
            if tile.is_wild:
                wilds.append(i)
        return wilds

    def get_value(self):
        total = 0
        value = 0
        if self.set():
            for tile in self.tiles:
                if tile.number > value:
                    value = tile.number
                total += tile.number
            if self.contains_wild:
                total += value * len(self.get_wild_index())
        elif self.run():
            for tile in self.tiles:
                total += tile.number
            if self.contains_wild:
                wilds = self.get_wild_index()
                #for i in range(len(wilds)):
                if len(wilds) > 1:
                    if wilds[0] == wilds[1] - 1:
                        try:
                            total += self.tiles[wilds[0] + 2].number - 2
                            total += self.tiles[wilds[0] + 2].number - 1
                        except IndexError:
                            total += self.tiles[wilds[0] - 1].number + 1
                            total += self.tiles[wilds[0] - 1].number + 2
                    else:
                        try:
                            total += self.tiles[wilds[0] + 1].number - 1
                            total += self.tiles[wilds[0] - 1].number + 1
                        except IndexError:
                            total += self.tiles[wilds[0] + 1].number - 1
                            total += self.tiles[wilds[0] + 1].number - 1
                else:
                    try:
                        total += self.tiles[wilds[0] + 1].number - 1
                    except IndexError:
                        total += self.tiles[wilds[0] - 1].number + 1
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

    # 3-6  tiles of the same number, different colors (wilds included)
    def set(self):
        valid_set = False
        colors = []
        num = []
        wilds = 0
        for tile in self.tiles:
            if tile.is_wild:
                wilds += 1
                print(f"wild tile seen num wilds = {wilds}")
            elif tile.color not in colors:
                colors.append(tile.color)

        # if num of colors == num of tiles return true
        if len(colors) == len(self.tiles) and len(self.tiles) > 2:
            print(f"length of set tiles is {len(self.tiles)}")
            valid_set = True
        # if num of colors != num of tiles
        else:
             if len(self.tiles) == 3:
                 # 3 tiles, two diff colors, 1 wild
                 if len(colors) == 2 and wilds == 1:
                     valid_set = True
                 # 3 tiles, 1 color, 2 wilds
                 if len(colors) == 1 and wilds == 2:
                     valid_set = True
             elif len(self.tiles) == 4:
                 # 4 tiles, three diff colors, 1 wild
                 if len(colors) == 3 and wilds == 1:
                     valid_set = True
                 # 4 tiles, 2 color, 2 wilds
                 if len(colors) == 2 and wilds == 2:
                     valid_set = True
        for tile in self.tiles:  # check that all tiles have the same number
            if tile.is_wild:
                pass
            elif tile.number not in num:
                num.append(tile.number)

        if len(num) == 1 and valid_set:
            return True
        else:
            return False


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