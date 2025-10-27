import arcade
from classes.gridboard import *
from classes.tile import Tile
import utils
import random

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # create grid of gameboard and Dock object, linked to grid
        self.grid = Grid()
        self.dock = Dock(self.grid)

        # create list of tile sprites (which will use quinn's tiles)
        self.tile_list = arcade.SpriteList()

        #keeping track of how many tiles are in play/left in the deck
        self.num_dealt = 0
        self.in_hand = 0

        self.held_tiles = None
        self.held_tiles_original_position = None

        self.pass_button = Button(50, 50, arcade.color.GREEN,
                             27, 125, "Pass")

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

    def deal_tile(self):
        if len(self.tile_list) < 1 or self.in_hand > 47: #max that can fit in dock is 48
            return False
        if self.in_hand < 24:
            peg = self.dock.board.peg_sprite_list[self.in_hand - 24] #start of dock is currently index -24?
        else:
            peg = self.dock.board.peg_sprite_list[self.in_hand - 72]  #second row of dock starts at index - 48
        self.tile_list[self.num_dealt].position = peg.center_x, peg.center_y
        self.num_dealt += 1
        self.in_hand += 1

    def setup(self):
        self.build_deck(35, 55)
        self.tile_list.shuffle()
        for _ in range(STARTING_TILE_AMT):
            self.deal_tile()

    # Draws the gameboard grid
    def on_draw(self):
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw the grid sprites
        self.grid.peg_sprite_list.draw()

        # draw the center points of each grid square
        for s in self.grid.peg_sprite_list:
            arcade.draw_point(s.center_x, s.center_y, arcade.color.WHITE, size=5)

        # draw the tiles
        self.tile_list.draw()

        # draw the pass button
        #self.pass_button.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

        # indicate pass_button was selected
        """pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.GREEN)
            #self.pass_button.pressed = True
            for tile in self.tile_list:
                print(tile.start_of_turn_x)
                if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                    tile.center_x = tile.start_of_turn_x
                    tile.center_y = tile.start_of_turn_y
                    # set the start of turns back to 0 meaning "unchanged"
                    tile.start_of_turn_x = 0
                    tile.start_of_turn_y = 0"""


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        if len(self.held_tiles) == 0:
            return

        peg, distance = arcade.get_closest_sprite(self.held_tiles[0], self.grid.peg_sprite_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.occupied:
            # For each held tile, move it to the pile we dropped on
            for i, dropped_card in enumerate(self.held_tiles):
                # Move tiles to proper position
                dropped_card.position = peg.center_x, peg.center_y

                # There is a tile on the peg
                peg.toggle_occupied()
                peg.Tile = dropped_card

            # Success, don't reset position of tiles
            reset_position = False

        if arcade.check_for_collision(self.held_tiles[0], peg) and peg.occupied:
            occupied_tile = peg.occupied

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset each tile's position
            # to its original spot.
            for tile_index, card in enumerate(self.held_tiles):
                card.position = self.held_tiles_original_position[tile_index]

        # empty out held tile list
        self.held_tiles = []

        # revert pass button color
        self.pass_button.set_color(arcade.color.OLIVE)
        #self.pass_button.passed = False

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

        if len(tiles) > 0:
            primary_tile = tiles[-1]

            # All other cases, grab the tile we are clicking on
            self.held_tiles = [primary_tile]
            # Save the position
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_tiles[0])

            # Bookmark the starting x and y when you pick up a tile ONLY ON FIRST TIME GRABBING TILE
            if primary_tile.start_of_turn_x == 0 and primary_tile.start_of_turn_y == 0:
                print(f"Current center x of primary tile: {primary_tile.center_x}")
                primary_tile.set_start_of_turn_pos(primary_tile.center_x, primary_tile.center_y)
                print(f"Start of turn pos of primary Tile: {primary_tile.start_of_turn_x}")

            # mark the peg as available again
            nearest_peg = self.grid.get_nearest_peg(self.held_tiles[0])
            if nearest_peg.occupied:
                nearest_peg.toggle_occupied()

    def on_key_press(self, symbol: int, modifiers: int):
        # for now if user press' S reset tiles to O.G. Poss
        if symbol == arcade.key.S:
            for tile in self.tile_list:
                if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                    # look through all pegs to find where tile was sitting (before we move it)
                    # then set that peg to unocupied before we move it back.
                    # TODO: make this more efficient
                    for peg in self.grid.peg_sprite_list:
                        if peg.center_x == tile.center_x and peg.center_y == tile.center_y:
                            peg.toggle_occupied()
                            break
                    tile.center_x = tile.start_of_turn_x
                    tile.center_y = tile.start_of_turn_y
                    # TODO: make this more efficient
                    # this is setting the place where the tile is moving to occupied.
                    for peg in self.grid.peg_sprite_list:
                        if peg.center_x == tile.center_x and peg.center_y == tile.center_y:
                            peg.toggle_occupied()
                            break
                    # set the start of turns back to 0 meaning "unchanged"
                    tile.start_of_turn_x = 0
                    tile.start_of_turn_y = 0
            print("Turn Rebased")

        if symbol == arcade.key.E:
            for tile in self.tile_list:
                tile.start_of_turn_x = 0
                tile.start_of_turn_y = 0
            print("Turn Ended")

        if symbol == arcade.key.D:
            # draw functionality
            pass
        # This sets all start of turn values back to 0
        # This is to "End your turn and move on to a "new turn" and is helpful for testing"