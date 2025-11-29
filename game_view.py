"""File containing GameView, WinView, and LoseView, the three screens of the game"""
import arcade
import arcade.gui

from deck import Deck
from utils import (WINDOW_WIDTH, WINDOW_HEIGHT, OUTER_MARGIN, INNER_MARGIN,
                   TILE_HEIGHT, NUM_TILE_VALUES, draw_instructions_screen, AI_DOCK_XPOS, AI_DOCK_YPOS, PASS_BUTTON_POS,
                   BUTTON_X, BUTTON_Y, END_TURN_BUTTON_POS)
from utils import STARTING_TILE_AMT, COLORS, TILE_SCALE, COLUMN_COUNT_DOCK, NUM_TILES
from gameboard import Gameboard
from game_components import Button, ButtonRect
from tile import Tile
from collection import Collection
from ai_player import Player

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        #initialize timer for turns
        self.time = 30
        self.timer_text = None

        self.player_first_melt = True
        self.ai_first_melt = True

        # ------------- Initialize game components ------------- #
        self.gameboard = Gameboard()

        # Initialize tiles
        self.tile_list = arcade.SpriteList()

        # tiles currently held by mouse
        self.held_tiles = []
        self.held_tiles_original_position = []

        self.build_deck()
        self.tile_list.shuffle()

        self.deck = Deck(self.tile_list)

        self.ai_player = Player()
        self.ai_num_turns = 0


        # give each player 14 initial tiles
        for _ in range(STARTING_TILE_AMT):
            self.deal_tile_user()
            self.deal_tile_to_ai(self.ai_player)

        # flag to show instructions
        self.show_instructions = False

        # marker displaying num of tiles the ai player has in their hand
        self.counter = arcade.XYWH(x=AI_DOCK_XPOS, y=AI_DOCK_YPOS, width=30, height=200)
        self.lbl = arcade.Text(
            f"{self.deck.ai_hand}",
            x=AI_DOCK_XPOS-10,
            y=AI_DOCK_YPOS,
            color=arcade.color.WHITE,
            font_size=12
        )
        self.update_deck()

    def save_turn(self):
        for tile in self.tile_list:
            # reset the start of turn positions for the tiles
            tile.start_of_turn_x = 0
            tile.start_of_turn_y = 0

        # decrement count in player hand appropriately
            if tile.start_in_dock != tile.in_dock:
                tile.start_in_dock = tile.in_dock
        self.update_deck()

        if self.deck.user_hand == 0:
            self.window.show_view(WinView())
        print("Turn Saved")

    def end_turn(self):
        played = False
        for tile in self.tile_list:
            if tile.start_in_dock and not tile.in_dock:
                played = True
                break

        if played and self.check_valid_collections(self.player_first_melt):
            self.save_turn()
            if self.player_first_melt:
                self.player_first_melt = False

        elif played and not self.check_valid_collections(self.player_first_melt):
            self.roll_back()
            self.deal_tile_user()
        else:
            self.deal_tile_user()

        # TODO: create an update deck function and call here
        self.update_deck()

        # call ai turn
        self.ai_turn(self.ai_player)

    def update_deck(self):
        print("Updating Deck...")
        self.deck.update_user_hand(self.gameboard.user_dock.get_num_occupied_pegs())
        self.deck.update_ai_hand(len(self.ai_player.hand))
        self.deck.update_on_board(self.gameboard.grid.get_num_occupied_pegs())

        # remaining in deck
        self.deck.remainder_in_deck = (
                len(self.tile_list) - self.deck.on_board - self.deck.ai_hand - self.deck.user_hand
        )
        print(self.deck)
        print()


    # Resets the position of tiles to their placement one turn before
    def roll_back(self):
        for tile in self.tile_list:
            if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                if tile.start_in_dock and not tile.in_dock:
                    tile.in_dock = True

                # look through all pegs to find where tile was sitting (before we move it)
                # then set that peg to unoccupied before we move it back.
                for peg in self.gameboard.all_pegs:
                    if peg.center_x == tile.center_x and peg.center_y == tile.center_y:
                        peg.empty_peg()
                        break
                tile.center_x = tile.start_of_turn_x
                tile.center_y = tile.start_of_turn_y

                # this is setting the place where the tile is moving to occupied.
                for peg in self.gameboard.all_pegs:
                    if peg.center_x == tile.center_x and peg.center_y == tile.center_y:
                        peg.occupy_peg(tile)
                        break
                # set the start of turns back to 0 meaning "unchanged"
                tile.start_of_turn_x = 0
                tile.start_of_turn_y = 0
        self.update_deck()
        print("Turn Rebased")

    # creates all possible tiles and puts them in a deck
    def build_deck(self):
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

# ============================= AI FUNCTIONS ================================ #
    def find_placement_loc(self, col, ai_player):
        """Find available placement locations for a collection"""
        if not col:
            return []
        # Add 2 for the left and right buffer spaces, we wil return the list w/o these
        collection_length = len(col.tiles) + 2
        for row in self.gameboard.grid.peg_sprites:
            free_pegs = []
            for peg in row:
                if not peg.is_occupied():
                    free_pegs.append(peg)
                    if len(free_pegs) >= collection_length:
                        return free_pegs[1:-1]
                else:
                    free_pegs = []
        return []

    def ai_turn(self, ai_player):
        if ai_player.can_play():
            collection = ai_player.get_best_collection()
            if not self.ai_first_melt or (self.ai_first_melt and collection.get_value() >= 30):
                free_pegs = self.find_placement_loc(collection, ai_player)
                if free_pegs:
                    str = f"Ai player placing collection...\n"
                    for t in collection.tiles:
                        str += f"{t}, "
                    print(str)
                    for i in range(len(free_pegs)):
                        self.ai_move_tile(free_pegs[i], collection.tiles[i])
                    self.ai_player.played()
            else:
                self.deal_tile_to_ai(ai_player)
        else:
            self.deal_tile_to_ai(ai_player)

        #update GUI
        self.lbl = arcade.Text(
            f"{len(self.ai_player.hand)}",
            x=AI_DOCK_XPOS - 10,
            y=AI_DOCK_YPOS,
            color=arcade.color.WHITE,
            font_size=12
        )
        self.ai_num_turns += 1
        print(f"ai turn count: {self.ai_num_turns}\n")
        self.update_deck()

        if self.deck.ai_hand == 0:
            self.window.show_view(LoseView())

    def ai_move_tile(self, peg, tile):
        # 1st un-occupy the o.g. tile loc -> pass in coords of tile to get peg
        old_peg = self.get_peg_at(tile.center_x, tile.center_y)
        if old_peg is not None:
            old_peg.empty_peg()

        # 2nd Occupy peg and move tile
        peg.occupy_peg(tile)
        tile.center_x = peg.center_x
        tile.center_y = peg.center_y
        tile.in_ai_hand = False
        self.update_deck()

    def deal_tile_user(self):
        if (self.deck.remainder_in_deck < 1 or
                self.gameboard.user_dock.get_num_available_pegs() == 0 or
                self.deck.count_used_tiles() >= NUM_TILES):
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

        tile = self.tile_list[self.deck.count_used_tiles()]

        tile.position = peg.center_x, peg.center_y
        peg.occupy_peg(tile)

        print(f"Dealing tile {tile} to user...")
        self.update_deck()
        return True

    def deal_tile_to_ai(self, player):
        if self.deck.remainder_in_deck < 1 or len(player.hand) == player.hand_capacity:
            print("ERROR. Tile cannot be dealt")
            return False

        tile = self.tile_list[self.deck.count_used_tiles()]
        player.deal(tile)

        print(f"Dealing tile {tile} to ai...")
        self.update_deck()
        return True

# ======================= BOARD FUNCTIONS ================================== #
    def on_draw(self):
        # We should always start by clearing the window pixels
        self.clear()
        self.gameboard.draw()

        # Batch draw the grid sprites
        self.gameboard.all_pegs.draw()

        for peg in self.gameboard.all_pegs:
            arcade.draw_point(peg.center_x, peg.center_y, arcade.color.WHITE, size=5)

        # draw the tiles
        self.tile_list.draw()

        # draw the timer
        self.timer_text.draw()

        arcade.draw_rect_filled(self.counter, color=arcade.color.COPPER)
        self.lbl.draw()

        if self.show_instructions:
            draw_instructions_screen(self)


    def on_mouse_press(self, x, y, button, modifiers):
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

        # indicate pass_button was selected
        pos = [x, y]
        if self.gameboard.pass_button.is_clicked(pos):
            self.gameboard.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            self.end_turn()
            self.time = 30

        elif self.gameboard.end_turn_button.is_clicked(pos):
            self.gameboard.end_turn_button.set_color(arcade.color.NAVY_BLUE)
            self.end_turn()
            self.time = 30

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        # revert pass button color
        if self.gameboard.pass_button.is_clicked([x, y]):
            self.gameboard.pass_button.set_color(arcade.color.GREEN)
        if self.gameboard.end_turn_button.is_clicked([x, y]):
            self.gameboard.end_turn_button.set_color(arcade.color.HONOLULU_BLUE)

        if len(self.held_tiles) == 0:
            return
        else:
            self.user_drop_tile()
        self.update_deck()

    def user_drop_tile(self):
        peg, _ = arcade.get_closest_sprite(self.held_tiles[0], self.gameboard.all_pegs)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.tile:
            # For each held tile, move it to the pile we dropped on
            primary_tile = self.held_tiles[0]

            if peg.placement == "dock" and not primary_tile.start_in_dock:
                reset_position = True
            elif peg.placement == "dock" and primary_tile.start_in_dock:
                # Move tiles to proper position
                primary_tile.position = peg.center_x, peg.center_y

                # There is a tile on the peg
                p = arcade.get_sprites_at_point(primary_tile.position, self.gameboard.all_pegs)[-1]

                p.occupy_peg(primary_tile)
                print(p)

                # Success, don't reset position of tiles
                reset_position = False
            else:
                if peg.placement == "grid":
                    primary_tile.in_dock = False

                # Move tiles to proper position
                primary_tile.position = peg.center_x, peg.center_y

                # There is a tile on the peg
                p = arcade.get_sprites_at_point(primary_tile.position, self.gameboard.all_pegs)[-1]

                p.occupy_peg(primary_tile)
                print(p)

                # Success, don't reset position of tiles
                reset_position = False

        if reset_position:
            self.revert_revert()

        # empty out held tile list
        self.held_tiles = []
        self.update_deck()

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

        self.update_deck()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for tile in self.held_tiles:
            tile.center_x += dx
            tile.center_y += dy

    def on_update(self, delta_time):
        self.time -= delta_time
        self.timer_text = arcade.Text(
            f"{self.time: .0f}",
            WINDOW_WIDTH - OUTER_MARGIN * 2 - INNER_MARGIN * 2,
            TILE_HEIGHT * 2.4,
            arcade.color.BLACK,
            12,
            anchor_x="center",
            anchor_y="center",
            font_name="Belwe Bold",
        )
        if self.time <= 0:
            self.end_turn()
            #TODO: ai turn goes here?
            self.time = 30

    def pull_to_top(self, tile: arcade.Sprite):
        """ Pull tile to top of rendering order (last to render, looks on-top) """
        self.tile_list.remove(tile)
        self.tile_list.append(tile)

    def pick_up_tile(self, x, y):
        tiles = arcade.get_sprites_at_point((x, y), self.tile_list)
        pegs = arcade.get_sprites_at_point((x, y), self.gameboard.all_pegs)

        if len(tiles) > 0:
            primary_tile = tiles[-1]

            if pegs:
                associated_peg = pegs[-1]
                associated_peg.empty_peg()
                print(associated_peg)

            # All other cases, grab the tile we are clicking on
            self.held_tiles = [primary_tile]
            # Save the position
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_tiles[0])

            # Bookmark the starting x and y when you pick up a tile ONLY ON FIRST TIME GRABBING TILE
            if primary_tile.start_of_turn_x == 0 and primary_tile.start_of_turn_y == 0:
                primary_tile.set_start_of_turn_pos(primary_tile.center_x, primary_tile.center_y)
        self.update_deck()

    def get_peg_at(self, x_coord, y_coord):
        # Use this function to get a peg from the two given coords
        for row in self.gameboard.grid.peg_sprites:
            for peg in row:
                if peg.center_x == x_coord and peg.center_y == y_coord:
                    return peg
        return None

    #first melt logic: collections must have been fully placed from players dock
    def check_valid_collections(self, first_melt):
        open_collection = False
        empty = True
        reset = False
        moved = False
        first_sum = 0
        first_placed = False
        # 4 cases, each peg is ONE of these...
        for row in self.gameboard.grid.peg_sprites:
            collection = Collection()
            open_collection = False
            for peg in row:
                # same collection logic here
                # Only looking at pegs in grid
                if peg.placement == "grid":
                    # if there is a tile ... and no current collection
                    if peg.is_occupied() and not open_collection:
                        collection.add(peg.get_tile())
                        open_collection = True
                        empty = False
                        if first_melt and peg.get_tile().start_in_dock:
                            first_placed = True
                        if peg.get_tile().start_of_turn_x != 0:
                            moved = True
                            #first_sum += peg.get_tile().number
                        else:
                            moved = False

                    # if there is a tile ... and a curr collection
                    elif peg.is_occupied() and open_collection:
                        collection.add(peg.get_tile())
                        # if there is a mix of player's tiles and tiles that were already on the board,
                        # return false
                        if first_melt and first_placed and not peg.get_tile().start_in_dock:
                            return False
                        elif first_melt and not first_placed and peg.get_tile().start_in_dock:
                            return False

                    # if there is NO tile ... and a curr collection
                    elif not peg.is_occupied() and open_collection:
                        # print("No tile, open collection")
                        # close the collection
                        open_collection = False
                        if first_melt and first_placed:
                            first_sum += collection.get_value()
                        if not collection.is_valid():
                            # if collection is invalid, bounce tiles
                            return False
                        else:
                            collection.clear()
                            first_placed = False
                #if len(collection.tiles) > 0 and collection.get_value() > first_sum:
                    #first_sum = collection.get_value()
        if first_melt and first_sum < 30:
            return False
        return True

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.U:
            self.roll_back()

        elif symbol == arcade.key.S:
            self.end_turn()

        elif symbol == arcade.key.D:
            self.deal_tile_user()

        elif symbol == arcade.key.W:
            self.num_user_hand = 0
            self.window.show_view(WinView())

        elif symbol == arcade.key.L:
            self.num_user_hand = 1
            self.window.show_view(LoseView())

        elif symbol == arcade.key.Q:
            self.check_valid_collections(self.player_first_melt)

        # press H to toggle help/instructions
        elif symbol == arcade.key.H:
            self.show_instructions = not self.show_instructions

        elif symbol == arcade.key.K:
            self.gameboard.cheatsheet.show_keybinds = not self.gameboard.cheatsheet.show_keybinds




""" ==================== Start and End Game Screens ==================== """

class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.start = Button(100, arcade.color.LEMON_CHIFFON,
                                 [WINDOW_WIDTH / 4,
                                  WINDOW_HEIGHT / 4],
                                 "Start Game!")

        self.rules = Button(100, arcade.color.LEMON_CHIFFON, [WINDOW_WIDTH * 3 / 4,
                                                             WINDOW_HEIGHT / 4], "Rules")

        arcade.load_font("misc/belwebold.otf")
        self.text = arcade.Text("Welcome to", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4,
                                arcade.color.WHITE, 65, anchor_x="center", anchor_y="center",
                                font_name="Belwe Bold")

        self.show_instructions = False
        self.texture = arcade.load_texture("./misc/rummikub.png", )
        self.logo_sprite = arcade.Sprite(self.texture, scale=.9)

    def on_draw(self):
        self.clear()
        self.start.draw()
        arcade.draw_sprite(self.logo_sprite)
        self.logo_sprite.center_y = WINDOW_HEIGHT - 350
        self.logo_sprite.center_x = WINDOW_WIDTH / 2
        self.rules.draw()
        self.text.draw()
        if self.show_instructions:
            draw_instructions_screen(self)


    def on_mouse_press(self, x, y, button, modifiers):
        pos = [x, y]
        if self.start.is_clicked(pos):
            self.start.set_color(arcade.color.LIGHT_KHAKI)
            game_view = GameView()
            self.window.show_view(game_view)
        if self.show_instructions:
            self.show_instructions = False
        elif self.rules.is_clicked(pos):
            self.show_instructions = not self.show_instructions
            if self.show_instructions:
                draw_instructions_screen(self)

class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.OLIVINE
        self.play_again = Button(100, arcade.color.LEMON_CHIFFON,
                                 [WINDOW_WIDTH / 4,
                                 WINDOW_HEIGHT / 4],
                                 "Play Again")

        self.quit = Button(100, arcade.color.LEMON_CHIFFON, [WINDOW_WIDTH * 3/4,
                           WINDOW_HEIGHT / 4],"Quit Game")

        self.text = arcade.Text("You Won!", WINDOW_WIDTH /2, WINDOW_HEIGHT * 3/4,
                                arcade.color.BLACK,75, anchor_x="center", anchor_y="center")

    def on_draw(self):
        self.clear()
        self.play_again.draw()
        self.quit.draw()
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pos = [x, y]
        if self.play_again.is_clicked(pos):
            self.play_again.set_color(arcade.color.LIGHT_KHAKI)
            game_view = GameView()
            self.window.show_view(game_view)

        if self.quit.is_clicked(pos):
            self.quit.set_color(arcade.color.LIGHT_KHAKI)
            arcade.exit()

class LoseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BABY_PINK
        self.play_again = Button(100, arcade.color.BITTERSWEET,
                                [WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4],"Play Again")

        self.quit = Button(100, arcade.color.BITTERSWEET,
                           [WINDOW_WIDTH * 3/4, WINDOW_HEIGHT / 4], "Quit Game")

        self.text = arcade.Text("You Lost!", WINDOW_WIDTH /2, WINDOW_HEIGHT * 3/4,
                                arcade.color.BLACK,75, anchor_x="center", anchor_y="center")

    def on_draw(self):
        self.clear()
        self.play_again.draw()
        self.quit.draw()
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pos = [x, y]
        if self.quit.is_clicked(pos):
            arcade.exit()
        if self.play_again.is_clicked(pos):
            self.play_again.set_color(arcade.color.LIGHT_KHAKI)
            game_view = GameView()
            self.window.show_view(game_view)
