from utils import *
from gameboard import Gameboard
from game_components import Button, ButtonRect
from tile import Tile
from ai_player import Player

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
        wild = [Tile("tiles/red_wild.png", scale=TILE_SCALE),
                Tile("tiles/black_wild.png", scale=TILE_SCALE)]
        for w_card in wild:
            w_card.center_x = -20
            w_card.center_y = -20
            self.tile_list.append(w_card)

    def __str__(self):
        user_h = "User hand: "
        ai_h = "AI hand: "
        for u in self.user_hand:
            user_h += f"{u} "
        for a in self.ai_hand:
            ai_h += f"{a} "
        return f"{user_h}\n{ai_h}"


class GameViewScratch():
    def __init__(self):
        # super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.gameboard = Gameboard()

        # initialize buttons
        self.pass_button = Button(50, arcade.color.GREEN, PASS_BUTTON_POS, "")
        self.button_text = (
            arcade.Text("Pass", BUTTON_X, BUTTON_Y, arcade.color.BLACK, 16,
                        anchor_x="center", anchor_y="center", font_name="Belwe Bold")
        )
        self.end_turn_button = (
            ButtonRect(100, 40, arcade.color.HONOLULU_BLUE, END_TURN_BUTTON_POS, "End turn")
        )

        self.ai_player = Player()

        # Initialize tiles
        self.deck = Deck()

        # give each player 14 initial tiles
        for _ in range(STARTING_TILE_AMT):
            self.deal_tile_u()
            self.deal_tile_ai()


    def deal_tile_u(self):
        if (len(self.deck.remainder_in_deck) < 1 or
            self.gameboard.user_dock.get_num_available_pegs() or
            self.deck.count_used_tiles() >= NUM_TILES
        ):
            print("ERROR. Tile cannot be dealt")
            return False

        peg = None
        found = False
        for space in self.gameboard.user_dock.peg_sprite_list[-COLUMN_COUNT_DOCK:]:
            if not space.is_occupied():
                peg = space
                found = True
                break
        if not found: #continuing to second row
            for space in self.gameboard.user_dock.peg_sprite_list[-COLUMN_COUNT_DOCK * 2:]:
                if not space.is_occupied():
                    peg = space
                    break

        tile = self.deck.tile_list[self.deck.count_used_tiles()]
        tile.position = peg.center_x, peg.center_y

        peg.occupy_peg(tile)
        self.deck.add_to_user(tile)
        return True

    def deal_tile_ai(self):
        if (len(self.deck.remainder_in_deck) < 1 or
            len(self.ai_player.hand) == self.ai_player.hand_capacity
        ):
            print("ERROR. Tile cannot be dealt")
            return False

        tile = self.deck.tile_list[self.deck.count_used_tiles()]
        self.ai_player.deal(tile)

        self.deck.add_to_ai(tile)
        return True


if __name__ == "__main__":
    view = GameViewScratch()
    print(view.deck)