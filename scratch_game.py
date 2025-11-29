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

    # toString for debugging
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

        # tiles currently held by user cursor
        self.held_tiles = []
        self.held_tiles_original_position = []


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

    def uturn(self):
        pass

    def aiturn(self):
        pass

    def on_mouse_press(self, x, y, _):
        # get any tiles that might be selected
        self.user_pick_up_tile(x, y)

        # indicate which button was selected
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.LINCOLN_GREEN)
        elif self.end_turn_button.is_clicked(pos):
            self.end_turn_button.press(pos)

        self.end_turn()
        self.time = 30

    def on_mouse_release(self, x: float, y: float, _):
        """ Called when the user presses a mouse button. """
        # revert pass button color
        if self.pass_button.is_clicked([x, y]):
            self.pass_button.set_color(arcade.color.GREEN)
        if self.end_turn_button.is_clicked([x, y]):
            self.end_turn_button.release()

        if len(self.held_tiles) == 0:
            return
        else:
            self.user_drop_tile()


    def user_drop_tile(self):
        peg, _ = arcade.get_closest_sprite(self.held_tiles[0], self.gameboard.all_pegs)
        reset_position = True

        # See if we are in contact with the closest empty peg
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.tile:
            # get the tile at the front of held_tiles list
            primary_tile = self.held_tiles[0]

            if peg.placement == "dock" and not primary_tile.start_in_dock:
                reset_position = True
            else:
                if peg.placement == "grid":
                    primary_tile.in_dock = False

                # Move tiles to proper position
                primary_tile.position = peg.center_x, peg.center_y

                # put tile on the peg
                p = arcade.get_sprites_at_point(primary_tile.position, self.gameboard.all_pegs)[-1]
                p.occupy_peg(primary_tile)

                # update deck accordingly
                self.deck.user_places_tile(primary_tile)
                print(p)

                # Success, don't reset position of tiles
                reset_position = False

        if reset_position:
            self.revert_revert()

        # empty out held tile list
        self.held_tiles = []

    def user_pick_up_tile(self, x, y):
        tiles = arcade.get_sprites_at_point((x, y), self.deck.tile_list)
        pegs = arcade.get_sprites_at_point((x, y), self.gameboard.all_pegs)

        if len(tiles) > 0:
            # Grab the tile we are clicking on
            primary_tile = tiles[-1]

            if pegs:
                associated_peg = pegs[-1]
                associated_peg.empty_peg()
                print(associated_peg)

            self.held_tiles = [primary_tile]
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top of drawing order
            self.pull_to_top(self.held_tiles[0])

            # Bookmark the starting x and y when you *first* pick up a tile
            if primary_tile.start_of_turn_x == 0 and primary_tile.start_of_turn_y == 0:
                primary_tile.set_start_of_turn_pos(primary_tile.center_x, primary_tile.center_y)

    # Reset each tile's position to its original spot
    def revert_revert(self):
        for tile_index, card in enumerate(self.held_tiles):
            card.position = self.held_tiles_original_position[tile_index]
            # make sure that the peg being returned to exists
            pegs = arcade.get_sprites_at_point(card.position, self.gameboard.all_pegs)

            if pegs:
                og_peg = pegs[-1]
                og_peg.occupy_peg(card)
                print(f"RE occuping peg {og_peg}")

    def pull_to_top(self, tile: arcade.Sprite):
        self.deck.tile_list.remove(tile)
        self.deck.tile_list.append(tile)


if __name__ == "__main__":
    view = GameViewScratch()
    print(view.deck)