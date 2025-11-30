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
from arcade import SpriteList
from collection import Collection
from utils import COLUMN_COUNT_DOCK, ROW_COUNT_DOCK


class Player:
    def __init__(self):
        self.hand = SpriteList()
        self.hand_capacity = COLUMN_COUNT_DOCK * ROW_COUNT_DOCK
        self.is_turn = False
        self.initial_melt = False

    def deal(self, tile):
        tile.in_ai_hand = True
        tile.start_in_dock = False
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
            wild_cards = []
            wild_used = 0

            all_sets = {}
            # add all tiles to set dictionary
            for tile in self.hand:
                if tile.is_wild:
                    wild_cards.append(tile)
                elif tile.number not in all_sets:
                    all_sets[tile.number] = [tile]
                else:
                    all_sets[tile.number].append(tile)

            for s in all_sets:
                col = Collection()
                # add all the tiles in initial set to a collection
                for tile in all_sets[s]:
                    col.add(tile)
                # add valid collections to dict

                if len(wild_cards) == 1:
                    col.add(wild_cards[wild_used])
                elif len(wild_cards) == 2:
                    col.add(wild_cards[wild_used])
                    col.add(wild_cards[wild_used])

                if col.is_valid():
                    collections[col] = col.get_value()


        def find_runs():
            self.sort_runs()
            wild_cards = []
            wild_used = 0

            all_vals = {}
            runs = {}
            for tile in self.hand:
                if tile.is_wild:
                    wild_cards.append(tile)
                elif tile.color not in all_vals:
                    all_vals[tile.color] = [tile]
                else:
                    all_vals[tile.color].append(tile)
            # list should be in ascending order so just running through it and seeing if next is +1
            for tile_lst in all_vals.values():
                col = Collection()
                for idx, tile in enumerate(tile_lst):
                    if idx == 0:
                        col.add(tile)
                    elif tile.number == tile_lst[idx - 1].number + 1:
                        col.add(tile)
                    elif wild_used < len(wild_cards) and tile_lst[idx - 1].number < 13:
                        col.add(wild_cards[wild_used])
                        wild_used += 1
                        if tile.number == tile_lst[idx - 1].number + 2:
                            col.add(tile)
                    else:
                        if col.is_valid():
                            runs[col] = col.get_value()
                        col.clear()
                        wild_used = 0
                if wild_used < len(wild_cards):
                    col.add(wild_cards[wild_used])
                if col.is_valid():
                    collections[col] = col.get_value()
                wild_used = 0

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
        if not cols:
            return False
        return True


    def played(self):
        col = self.get_best_collection()
        for tile in col.tiles:
            self.hand.remove(tile)

    def __repr__(self):
        """representation of player's hand for testing"""
        output = ""
        for tile in self.hand[:-1]:
            output += f"{tile}, "
        output += f"{self.hand[-1]}, "
        return output
