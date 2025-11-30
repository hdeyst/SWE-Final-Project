# Class to help keep track of all tile movement
class Deck:
    def __init__(self, tile_list):
        self.total_tiles = len(tile_list)

        self.user_hand = 0
        self.ai_hand = 0
        self.on_board = 0
        self.remainder_in_deck = len(tile_list)

    def count_used_tiles(self):
        return self.total_tiles - self.remainder_in_deck

    def update_user_hand(self, num):
        self.user_hand = num

    def update_ai_hand(self, num):
        self.ai_hand = num

    def update_on_board(self, num):
        self.on_board = num


    def __str__(self):
        return (f"Of {self.total_tiles} tiles, {self.remainder_in_deck} tiles remain in deck \n"
                f"In user hand: {self.user_hand} \n"
                f"AI hand: {self.ai_hand} \n"
                f"Number on board: {self.on_board} \n"
                f"Num used tiles: {self.count_used_tiles()} \n")
