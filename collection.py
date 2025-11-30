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
                if len(wilds) > 1:
                    # if there are two wild tiles and they are right next to e/o
                    if wilds[0] == wilds[1] - 1:
                        # grab value from tile after the wilds in the collection
                        try:
                            total += self.tiles[wilds[0] + 2].number - 2
                            total += self.tiles[wilds[0] + 2].number - 1
                        except IndexError:
                            total += self.tiles[wilds[0] - 1].number + 1
                            total += self.tiles[wilds[0] - 1].number + 2
                    else: #if the two wild tiles are seperated and have a tile in between them
                        total += self.tiles[wilds[0] + 1].number - 1
                        total += self.tiles[wilds[1] - 1].number + 1
                        #except IndexError:
                            #total += self.tiles[wilds[0] + 1].number - 1
                            #total += self.tiles[wilds[0] + 1].number - 1
                else:
                    try:
                        total += self.tiles[wilds[0] + 1].number - 1
                    except IndexError:
                        total += self.tiles[wilds[0] - 1].number + 1
        return total



    def clear(self):
        self.tiles.clear()
        self.contains_wild = False

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

        if len(self.tiles) < 3 or len(self.tiles) > 4:
            return False

        for tile in self.tiles:
            if tile.is_wild:
                wilds += 1
            elif tile.color not in colors:
                colors.append(tile.color)

        #checking that all non-wild tiles are diff colors
        if len(colors) == len(self.tiles):
            valid_set = True
        else:
            if len(self.tiles) == 3:
                if len(colors) == 2 and wilds == 1:
                    valid_set = True
                elif len(colors) == 1 and wilds == 2:
                    valid_set = True
            else:
                if len(colors) == 3 and wilds == 1:
                    valid_set = True
                if len(colors) == 2 and wilds == 2:
                    valid_set = True

        for tile in self.tiles:  # check that all tiles have the same number
            if tile.is_wild:
                pass
            elif tile.number not in num:
                num.append(tile.number)

        return len(num) == 1 and valid_set


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
                break

        for i, tile in enumerate(self.tiles): #get index of the non-wild tile
            if tile.number == 13 and i != len(self.tiles)-1:
                return False
            if tile.number == 12:
                if len(self.get_wild_index()) > 1 and i != len(self.tiles)-2:
                    return False
            if tile.number == 1 and i != 0:
                return False
            if tile.number == 2:
                if len(self.get_wild_index()) > 1 and i != 1:
                    return False

        non_wilds = 0
        wilds_end = False
        for i, name in enumerate(self.tiles): # check that all tiles have the same color
            if name.color != self.tiles[index].color:
                if name.is_wild:
                    pass
                else:
                    return False
            if name.is_wild:
                if wilds_end:
                    non_wilds += 1
            elif name.number == self.tiles[index].number + non_wilds:
                wilds_end = True
                non_wilds += 1
            else:
                return False
        return True

    def __repr__(self):
        rep = ""
        for tile in self.tiles:
            rep = rep + str(tile) + ", "
        return rep
