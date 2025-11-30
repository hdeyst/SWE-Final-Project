"""File containing collection class which holds logic for checking validity of sets and runs"""
from tile import Tile
from utils import TILE_SCALE

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
                    if wilds[0] == wilds[1] - 1: # if there are two wild tiles and they are right next to eachother
                        try: #grab the value from the tile after the wilds in the collection
                            total += self.tiles[wilds[0] + 2].number - 2
                            total += self.tiles[wilds[0] + 2].number - 1
                        except IndexError: #grab the value from the value before the wilds in the collection
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
                break

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
                pass
            elif name.number == self.tiles[index].number + non_wilds:
                wilds_end = True
                non_wilds += 1
                pass
            else:
                return False
            """   
            if i > 0 and not self.tiles[i - 1].number + 1 == name.number:
                if name.is_wild or (self.tiles[i - 1].is_wild and name.number == (self.tiles[index].number - difference)):
                    pass
                else:
                    return False"""
        if self.tiles[index].number + non_wilds > 13:
            return False
        return True

    def __repr__(self):
        rep = ""
        for tile in self.tiles:
            rep = rep + str(tile) + ", "
        return rep

    def test_runs(self):
        red2 = Tile(f"tiles/red_2.png", scale=TILE_SCALE)
        red3 = Tile(f"tiles/red_3.png", scale=TILE_SCALE)
        red4 = Tile(f"tiles/red_4.png", scale=TILE_SCALE)
        wild = Tile("tiles/red_wild.png", scale=TILE_SCALE)
        yellow2 = Tile(f"tiles/yellow_2.png", scale=TILE_SCALE)
        yellow3 = Tile(f"tiles/yellow_3.png", scale=TILE_SCALE)
        black2 = Tile(f"tiles/black_2.png", scale=TILE_SCALE)
        black5 = Tile(f"tiles/black_5.png", scale=TILE_SCALE)

        # testing sets
        wrong1 = Collection()
        wrong1.add(yellow2)
        wrong1.add(yellow3)

        wrong2 = Collection()
        wrong2.add(black2)
        wrong2.add(black5)

        wrong3 = Collection()
        wrong3.add(black2)
        wrong3.add(wild)
        wrong3.add(black5)

        wrong4 = Collection()
        wrong4.add(black2)
        wrong4.add(black5)
        wrong4.add(wild)

        right1 = Collection()
        right1.add(yellow2)
        right1.add(yellow3)
        right1.add(wild)

        right2 = Collection()
        right2.add(red2)
        right2.add(red3)
        right2.add(red4)

        run_tests = [wrong1, wrong2, wrong3, wrong4, right1, right2]
        for test in run_tests:
            print(f"{test}: {test.run()}")

    def test_sets(self):
        red2 = Tile(f"tiles/red_2.png", scale=TILE_SCALE)
        red3 = Tile(f"tiles/red_3.png", scale=TILE_SCALE)
        red4 = Tile(f"tiles/red_4.png", scale=TILE_SCALE)
        wild = Tile("tiles/red_wild.png", scale=TILE_SCALE)
        yellow2 = Tile(f"tiles/yellow_2.png", scale=TILE_SCALE)
        yellow3 = Tile(f"tiles/yellow_3.png", scale=TILE_SCALE)
        black2 = Tile(f"tiles/black_2.png", scale=TILE_SCALE)
        black5 = Tile(f"tiles/black_5.png", scale=TILE_SCALE)

        # testing sets
        wrong1 = Collection()
        wrong1.add(yellow2)
        wrong1.add(red2)

        wrong2 = Collection()
        wrong2.add(red2)
        wrong2.add(red3)
        wrong2.add(red4)

        wrong3 = Collection()
        wrong3.add(black2)
        wrong3.add(wild)

        wrong4 = Collection()
        wrong4.add(black2)
        wrong4.add(red4)
        wrong4.add(wild)

        wrong5 = Collection()
        wrong5.add(black2)
        wrong5.add(wild)
        wrong5.add(red4)

        right1 = Collection()
        right1.add(yellow2)
        right1.add(red2)
        right1.add(wild)

        right2 = Collection()
        right2.add(red2)
        right2.add(yellow2)
        right2.add(black2)

        set_tests = [wrong1, wrong2, wrong3, wrong4, wrong5, right1, right2]
        for test in set_tests:
            print(f"{test}: {test.set()}")

if __name__ == "__main__":
    collection = Collection()
    print("Sets: 5 false, 2 true")
    collection.test_sets()
    #print("\nRuns: 4 false, 2 true")
    #collection.test_runs()