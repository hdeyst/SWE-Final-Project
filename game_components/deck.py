import arcade

from utils import TILE_SCALE, NUM_TILE_VALUES, COLORS
from tile import Tile

# Class to help keep track of all tile movement
class Deck:
    def __init__(self):
        # Initialize tiles
        self.tile_list = arcade.SpriteList()
        self.build_deck_()
        self.tile_list.shuffle()

        self.user_hand = []
        self.ai_hand = []
        self.on_board = []
        self.remainder_in_deck = self.tile_list

    def add_to_user(self, tile):
        self.user_hand.append(tile)
        self.remainder_in_deck.remove(tile)

    def add_to_ai(self, tile):
        self.ai_hand.append(tile)
        self.remainder_in_deck.remove(tile)

    def user_places_tile(self, tile):
        self.on_board.append(tile)
        self.user_hand.remove(tile)

    def ai_places_tile(self, tile):
        self.on_board.append(tile)
        self.ai_hand.remove(tile)

    def count_used_tiles(self):
        return len(self.tile_list) - len(self.remainder_in_deck)

    def build_deck_(self):
        for color in COLORS:
            for j in range(NUM_TILE_VALUES):
                # there are two of each type of tile in the deck
                for _ in range(2):
                    tile = Tile(f"tiles/{color}_{j + 1}.png", scale=TILE_SCALE)
                    # Stacked tile placement, places all tiles in the corner stacked on one another
                    tile.center_x = -20
                    tile.center_y = -20
                    self.tile_list.append(tile)

        # add wild cards to the deck
        wild = [Tile("../tiles/red_wild.png", scale=TILE_SCALE),
                Tile("../tiles/black_wild.png", scale=TILE_SCALE)]
        for w_card in wild:
            w_card.center_x = -20
            w_card.center_y = -20
            self.tile_list.append(w_card)

    def draw(self):
        self.tile_list.draw()

    # toString for debugging
    def __str__(self):
        user_h = "User hand: "
        ai_h = "AI hand: "
        for u in self.user_hand:
            user_h += f"{u} "
        for a in self.ai_hand:
            ai_h += f"{a} "
        return f"{user_h}\n{ai_h}"