class Tile:
    def __init__(self, num, col):
        self.number = num
        self.color = col

class Collection:
    def __init__(self, item): #assuming a collection will be created whenever a tile is added to the board alone
        self.tiles = [item]

    def add(self, item, index):
        self.tiles.insert(index, item) #ensuring the list will be in the same order as on the board
                                       #could use positions to determine order if we want to make Tile less abstract?

    def remove(self, item):
        self.tiles.remove(item)

    def getValue(self):
        sum = 0
        for e in self.tiles:
            sum += e.number
        return sum

    def isSet(self):
        isSet = True
        for e in self.tiles:
            if e.number != self.tiles[0]:
                isSet = False
        return isSet
