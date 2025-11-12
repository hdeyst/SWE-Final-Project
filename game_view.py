"""File containing GameView, WinView, and LoseView, the three screens of the game"""
import arcade
import arcade.gui

from cheatsheet import Cheatsheet
from utils import WINDOW_WIDTH, WINDOW_HEIGHT, OUTER_MARGIN, INNER_MARGIN, TILE_HEIGHT, INSTRUCTIONS, CHEATSHEET_BOTTOM, \
    CHEATSHEET_WIDTH, CHEATSHEET_HEIGHT
from utils import STARTING_TILE_AMT, COLORS, TILE_SCALE, COLUMN_COUNT_DOCK
from gameboard import Gameboard
from gridboard import Button
from tile import Tile
from collection import Collection

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # initialize game components
        self.gameboard = Gameboard()

        self.pass_button = Button(
            50,
            arcade.color.GREEN,
            [WINDOW_WIDTH - OUTER_MARGIN * 2 - INNER_MARGIN * 2, TILE_HEIGHT * 2],
            "Pass"
        )
        self.pass_button.font_size = 14

        self.cheatsheet = Cheatsheet(
            left=OUTER_MARGIN,
            bottom=CHEATSHEET_BOTTOM,
            width=CHEATSHEET_WIDTH,
            height=CHEATSHEET_HEIGHT,
        )

        # Initialize tiles
        self.tile_list = arcade.SpriteList()

        self.used_tiles = [0, 0] # [num dealt, num in hand]

        self.held_tiles = None
        self.held_tiles_original_position = None

        self.build_deck(-10, -10)
        self.tile_list.shuffle()
        for _ in range(STARTING_TILE_AMT):
            self.deal_tile()

        # flag to show instructions
        self.show_instructions = False

    def save_turn(self):
        for tile in self.tile_list:
            tile.start_of_turn_x = 0
            tile.start_of_turn_y = 0
            if tile.start_in_dock != tile.in_dock:
                tile.start_in_dock = tile.in_dock
                self.used_tiles[1] -= 1
            if self.used_tiles[1] == 0:
                self.window.show_view(WinView())
        print("Turn Saved")

    def roll_back(self):
        # for now if user press' S reset tiles to O.G. Poss
        for tile in self.tile_list:
            if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
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
        print("Turn Rebased")

    # creates all possible tiles and puts them in a deck
    def build_deck(self, deck_x_pos, deck_y_pos):
        self.held_tiles = []
        self.held_tiles_original_position = []

        for color in COLORS:
            for j in range(13):

                tile = Tile(f"tiles/{color}_{j + 1}.png", scale=TILE_SCALE)
                # Stacked tile placement, places all tiles in the corner stacked on one another
                tile.center_x = deck_x_pos
                tile.center_y = deck_y_pos
                tile.start_of_turn_x = 0
                tile.start_of_turn_y = 0
                self.tile_list.append(tile)

                tile = Tile(f"tiles/{color}_{j + 1}.png", scale=TILE_SCALE)
                # Creating 2nd Tile for each
                tile.center_x = deck_x_pos
                tile.center_y = deck_y_pos
                tile.start_of_turn_x = 0
                tile.start_of_turn_y = 0
                self.tile_list.append(tile)

        tile = Tile(f"tiles/red_wild.png", scale = TILE_SCALE)
        self.tile_list.append(tile)
        tile = Tile(f"tiles/black_wild.png", scale=TILE_SCALE)
        self.tile_list.append(tile)



    def deal_tile(self):
        if len(self.tile_list) < 1 or self.used_tiles[1] >= COLUMN_COUNT_DOCK * 2:
            print("ERROR. Tile cannot be dealt")
            return False

        found = False
        for space in self.gameboard.dock.peg_sprite_list[-COLUMN_COUNT_DOCK:]:
            if not space.is_occupied():
                peg = space
                found = True
                break
        if not found: #continuing to second row
            for space in self.gameboard.dock.peg_sprite_list[-COLUMN_COUNT_DOCK * 2:]:
                if not space.is_occupied():
                    peg = space
                    break

        tile = self.tile_list[self.used_tiles[0]]

        tile.position = peg.center_x, peg.center_y
        peg.occupy_peg(tile)

        self.used_tiles[0] += 1
        self.used_tiles[1] += 1

        return True

    # Draws the gameboard grid
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

        # draw the pass button
        self.pass_button.draw()

        if self.show_instructions:
            self.draw_instructions_screen()

        self.cheatsheet.draw()



    def on_mouse_press(self, x, y, button, modifiers):
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

        # indicate pass_button was selected
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            self.roll_back()
            self.deal_tile()


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        # revert pass button color
        if self.pass_button.is_clicked([x, y]):
            self.pass_button.set_color(arcade.color.GREEN)

        if len(self.held_tiles) == 0:
            return

        peg, _ = arcade.get_closest_sprite(self.held_tiles[0], self.gameboard.all_pegs)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.tile:
            # For each held tile, move it to the pile we dropped on
            primary_tile = self.held_tiles[0]

            if peg.placement == "dock" and not primary_tile.start_in_dock:
                reset_position = True
            else:
                if peg.placement == "grid" and primary_tile.in_dock:
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
            # Where-ever we were dropped, it wasn't valid. Reset each tile's position
            # to its original spot.
            for tile_index, card in enumerate(self.held_tiles):
                card.position = self.held_tiles_original_position[tile_index]
                # make sure that the peg being returned to exists
                pegs = arcade.get_sprites_at_point(card.position, self.gameboard.all_pegs)

                if pegs:
                    og_peg = pegs[-1]
                    og_peg.occupy_peg(card)
                    print(f"RE occuping peg {og_peg}")

        # empty out held tile list
        self.held_tiles = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for tile in self.held_tiles:
            tile.center_x += dx
            tile.center_y += dy

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
                # print(primary_tile.center_x)
                primary_tile.set_start_of_turn_pos(primary_tile.center_x, primary_tile.center_y)
                # print(primary_tile.start_of_turn_x)

    def check_valid_collections(self):
        open_collection = False
        reset = False
        collection = Collection()
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
                        print("Tile, closed collection")
                        collection.add(peg.get_tile())
                        open_collection = True

                    # if there is a tile ... and a curr collection
                    elif peg.is_occupied() and open_collection:
                        # print("Tile, open collection")
                        # adds tile to the collection
                        collection.add(peg.get_tile())

                    # if there is NO tile ... and a curr collection
                    elif not peg.is_occupied() and open_collection:
                        # print("No tile, open collection")
                        # close the collection
                        open_collection = False
                        if not collection.is_valid():
                            # if collection is invalid, bounce tiles
                            self.roll_back()
                            reset = True
                            collection.clear()
                        else:
                            collection.clear()
        if not reset:
            self.save_turn()

    def button_press(self, x, y):
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            self.check_valid_collections()

    def draw_instructions_screen(self):
        background = arcade.XYWH(self.center_x, self.center_y, 700, 400)

        # color is "MIDNIGHT_GREEN" but the fourth value is transparency
        arcade.draw_rect_filled(rect=background, color=(0, 73, 83, 220))
        arcade.draw_rect_outline(rect=background, color=arcade.color.WHITE, border_width=2)

        start_y = self.center_y + 200
        for i, line in enumerate(INSTRUCTIONS):
            start_y -= 30
            txt = arcade.Text(line, self.center_x - 320, start_y, color=arcade.color.WHITE)
            txt.draw()

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.S:
            self.roll_back()

        elif symbol == arcade.key.E:
            self.save_turn()

        elif symbol == arcade.key.D:
            self.deal_tile()

        elif symbol == arcade.key.W:
            self.used_tiles[1] = 0
            self.window.show_view(WinView())

        elif symbol == arcade.key.L:
            self.used_tiles[1] = 1
            self.window.show_view(LoseView())

        elif symbol == arcade.key.Q:
            self.check_valid_collections()

        # press H to toggle help/instructions
        elif symbol == arcade.key.H:
            self.show_instructions = not self.show_instructions

        elif symbol == arcade.key.K:
            self.cheatsheet.show_keybinds = not self.cheatsheet.show_keybinds


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.start = Button(100, arcade.color.LEMON_CHIFFON,
                                 [WINDOW_WIDTH / 4,
                                  WINDOW_HEIGHT / 4],
                                 "Start Game!") #TODO should we add fonts

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
            self.draw_instructions_screen()

    def draw_instructions_screen(self):
        background = arcade.XYWH(self.center_x, self.center_y, 700, 400)

        # color is "MIDNIGHT_GREEN" but the fourth value is transparency
        arcade.draw_rect_filled(rect=background, color=(0, 73, 83, 220))
        arcade.draw_rect_outline(rect=background, color=arcade.color.WHITE, border_width=2)

        start_y = self.center_y + 200
        for i, line in enumerate(INSTRUCTIONS):
            start_y -= 30
            txt = arcade.Text(line, self.center_x - 320, start_y, color=arcade.color.WHITE)
            txt.draw()

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
                self.draw_instructions_screen()

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
        #TODO: should we save scores? any other data we would want saved?
        if self.play_again.is_clicked(pos):
            self.play_again.set_color(arcade.color.LIGHT_KHAKI)
            game_view = GameView()
            self.window.show_view(game_view)

