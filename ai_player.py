"""
AI-Player Class Description:

Properties:
    - hand (Tile_Collection)
    - is_turn (Boolean)
    - initial_melt (Boolean)
Functions:
    - "Check Hand"
    - "Check can lay down?"

"""
import arcade

from collection import Collection
from tile import Tile
from arcade import SpriteList
from utils import TILE_SCALE, COLUMN_COUNT_DOCK, ROW_COUNT_DOCK


class Player:
    def __init__(self):
        self.hand = SpriteList()
        self.hand_capacity = COLUMN_COUNT_DOCK * ROW_COUNT_DOCK
        self.is_turn = False
        self.initial_melt = False


    def deal(self, tile):
        self.hand.append(tile)

    def sort_sets(self):
        self.hand.sort(key=lambda tile: tile.color)
        self.hand.sort(key=lambda tile: tile.number)

    def sort_runs(self):
        self.hand.sort(key=lambda tile: tile.number)
        self.hand.sort(key=lambda tile: tile.color)

    # makes a new dictionary sp that when new tiles are added,
    # it can be refreshed w/ that in mind
    def create_collections(self):
        collections = {}

        def find_sets():
            # Add sets to dictionary
            self.sort_sets()

            all_sets = {}
            # add all tiles to set dictionary
            for tile in self.hand:
                if tile.number not in all_sets:
                    all_sets[tile.number] = [tile]
                else:
                    all_sets[tile.number].append(tile)

            for s in all_sets:
                col = Collection()
                # add all the tiles in initial set to a collection
                for tile in all_sets[s]:
                    col.add(tile)
                # add valid collections to dict
                if col.is_valid():
                    collections[col] = col.get_value()

        # TODO: if all the colors do not create one set, but there is
        #  a subset w/in, then it won't be recognized
        def find_runs():
            self.sort_runs()

            all_vals = {}
            for tile in self.hand:
                if tile.color not in all_vals:
                    all_vals[tile.color] = [tile]
                else:
                    all_vals[tile.color].append(tile)

            for r in all_vals:
                col = Collection()
                # add all the tiles in initial run to a collection
                for tile in all_vals[r]:
                    col.add(tile)
                # add valid collections to dict
                if col.is_valid():
                    collections[col] = col.get_value()

        # put it all together
        find_sets()
        find_runs()
        return collections


    def get_best_collection(self):
        cols = self.create_collections()
        if not cols:
            print("AI: No valid collections found. Drawing a tile instead.")
            return []
        best_coll = max(cols, key=cols.get)
        return best_coll

    def can_play(self):
        cols = self.create_collections()
        if cols == {}:
            return False
        else:
            return True

    def get_grid_tiles(self):
        grid_tiles = []
        for peg in self.gameboard.all_pegs:
            if peg.placement == "grid" and peg.is_occupied():
                grid_tiles.append((peg, peg.get_tile()))
        return grid_tiles


        #look through board until finding a space of size col_len + 2 (borders)
        # make sure space isn't a part of two lines (starting on one line and ending on the next)
        # return either a list of coords length col_len (only include the coords the tiles will acutally go on)
        #TODO: Alternatively we can just change this function to directry place the tiles


    def turn(self):
        if self.initial_melt:
            best_c = self.get_best_collection()
            if best_c.value() > 30:
                # TODO:
                #  place best collection on board first
                #  remove those tiles from player hand
                pass
            else:
                # TODO:
                #  draw tile
                #  mark end of turn
                return
        # continue placing tiles

        # while self.create_collections() != {}:
        #  play each collection, while updating the tiles in hand
        if self.create_collections() == {}:
            # TODO:
            #  draw tile
            #  mark end of turn
            return
        for c in self.create_collections():
            # TODO:
            #  play each collection
            #  remove those tiles from the players hand
            pass


    def __repr__(self):
        """representation of player's hand for testing"""
        output = ""
        for tile in self.hand[:-1]:
            output += f"{tile}, "
        output += f"{self.hand[-1]}, "
        return output

if __name__ == "__main__":
    red2 = Tile(f"tiles/red_2.png", scale = TILE_SCALE)
    red3 = Tile(f"tiles/red_3.png", scale = TILE_SCALE)
    red4 = Tile(f"tiles/red_4.png", scale = TILE_SCALE)
    yellow2 = Tile(f"tiles/yellow_2.png", scale = TILE_SCALE)
    yellow3 = Tile(f"tiles/yellow_3.png", scale = TILE_SCALE)
    black2 = Tile(f"tiles/black_2.png", scale = TILE_SCALE)
    black5 = Tile(f"tiles/black_5.png", scale = TILE_SCALE)

    player = Player()
    player.deal(yellow3)
    player.deal(black5)
    player.deal(red2)
    player.deal(yellow2)
    player.deal(black2)
    player.deal(red3)
    player.deal(red4)

    print(player)
    player.sort_sets()
    print(f"set sorted: {player}")
    player.sort_runs()
    print(f"run sorted: {player}")

    colls = player.create_collections()
    print(f"all collections:")
    for c in colls:
        print(f"{c}: {colls[c]}")

    print(f"best collection: {player.get_best_collection()}")
