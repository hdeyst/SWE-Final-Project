import arcade

from utils import TILE_SCALE, NUM_TILE_VALUES, COLORS
from tile import Tile

# Class to help keep track of all tile movement
class Deck:
    def __init__(self, tile_list):
        self.total_tiles = len(tile_list)

        self.user_hand = 0
        self.ai_hand = 0
        self.on_board = 0
        self.remainder_in_deck = len(tile_list)

    def add_to_user(self):
        self.user_hand += 1
        self.remainder_in_deck -= 1

    def add_to_ai(self):
        self.ai_hand += 1
        self.remainder_in_deck -= 1

    def user_places_tile(self):
        self.on_board += 1
        self.user_hand -= 1

    def ai_places_tile(self):
        self.on_board += 1
        self.ai_hand -= 1

    # invalid placement of tile
    def revert_to_user(self):
        self.on_board -= 1
        self.user_hand += 1

    def count_used_tiles(self):
        return self.total_tiles - self.remainder_in_deck

    def __str__(self):
        return (f"Of {self.total_tiles} tiles, {self.remainder_in_deck} tiles remain in deck \n"
                f"In user hand: {self.user_hand} \n"
                f"AI hand: {self.ai_hand} \n"
                f"Number on board: {self.on_board} \n"
                f"Num used tiles: {self.count_used_tiles()} \n")