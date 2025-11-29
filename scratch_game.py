from utils import *
from gameboard import Gameboard
from deck import Deck
from ai_player import Player

class GameViewScratch(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.gameboard = Gameboard()
        self.ai_player = Player()

        # Initialize tiles
        self.deck = Deck()
        for _ in range(STARTING_TILE_AMT):
            self.deal_tile_u()
            self.deal_tile_ai()

        # tiles currently held w/ user cursor
        self.held_tiles = []
        self.held_tiles_original_position = []

        # initialize timer for turns
        self.user_time = 30
        self.ai_time = 5 # makes for a better game experience if ai takes time
        self.timer_text = None

        # flag variables
        self.show_instructions = False
        self.player_first_melt = True
        self.ai_first_melt = True


    def deal_tile_u(self):
        if (len(self.deck.remainder_in_deck) < 1 or
            self.gameboard.user_dock.get_num_available_pegs() or
            self.deck.count_used_tiles() >= NUM_TILES
        ):
            print("ERROR. Tile cannot be dealt")
            return False

        # find a place in user dock for the tile
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

    def on_mouse_press(self, x, y, button, modifier) :
        # get any tiles that might be selected
        self.user_pick_up_tile(x, y)

        # indicate which button was selected
        pos = [x, y]
        if self.gameboard.pass_button.is_clicked(pos):
            self.gameboard.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            self.end_turn()
            self.time = 30

        elif self.gameboard.end_turn_button.is_clicked(pos):
            self.gameboard.end_turn_button.press(pos)
            self.end_turn()
            self.time = 30

    def on_mouse_release(self, x: float, y: float, button, modifier):
        """ Called when the user presses a mouse button. """
        # revert pass button color
        if self.gameboard.pass_button.is_clicked([x, y]):
            self.gameboard.pass_button.set_color(arcade.color.GREEN)
        if self.gameboard.end_turn_button.is_clicked([x, y]):
            self.gameboard.end_turn_button.release()

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


if __name__ == "__main__":
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameViewScratch()

    window.show_view(game)

    # Start the arcade game loop
    arcade.run()