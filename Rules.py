class Tile: #for testing of collection until Tile class is complete in front end
    def __init__(self, num, col):
        self.number = num
        self.color = col
        

class Collection:
    def __init__(self, tile): #assuming a collection will be created whenever a tile is added to the board alone
        self.tiles = [tile]
        self.isSet = True

    def add(self, tile, index):
        self.tiles.insert(index, tile) #ensuring the list will be in the same order as on the board
                                       #could use positions to determine order if we want to make Tile less abstract?

    def remove(self, item):
        self.tiles.remove(item)

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

#tests
if __name__ == "__main__":
    r0 = Tile(0, "red")
    b0 = Tile(0, "blue")
    g0 = Tile(0, "green")
    o0 = Tile(0, "orange")
    r1 = Tile(1, "red")
    r2 = Tile(2, "red")
    r3 = Tile(3, "red")

    group0 = Collection(r0) #all 0s, 3 different colors
    group0.add(g0, 1)
    group0.add(b0, 2)
    group0.add(o0, 3)

    group1 = Collection(r0)  #all 0s, 4 different colors
    group1.add(g0, 1)
    group1.add(b0, 2)
    group1.add(o0, 3)

    group2 = Collection(r0)  #all reds, [0,1,2,3]
    group2.add(r1, 1)
    group2.add(r2, 2)
    group2.add(r3, 3)


    print(group0.isValid())
    print(group1.isValid())
    print(group2.isValid())
