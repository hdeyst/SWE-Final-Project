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
from tile import Tile
from arcade import SpriteList
from utils import TILE_SCALE


class Player:
    def __init__(self):
        self.hand = SpriteList()
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