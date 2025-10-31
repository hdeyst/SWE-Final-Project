import arcade

from classes.gameboard import Gameboard
from classes.gridboard import *
from classes.tile import Tile
from classes.collection import Collection
import utils
import random

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        self.gameboard = Gameboard()

        # create list of tile sprites (which will use quinn's tiles)
        self.tile_list = arcade.SpriteList()

        #keeping track of how many tiles are in play/left in the deck
        self.num_dealt = 0
        self.in_hand = 0

        self.held_tiles = None
        self.held_tiles_original_position = None

        self.collections = []

        self.pass_button = Button(100, 100, arcade.color.GREEN,
                                  x_pos=WINDOW_WIDTH-OUTER_MARGIN*2-INNER_MARGIN*2,
                                  y_pos=TILE_HEIGHT*2,
                                  text="Pass")

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
            peg = self.gameboard.dock.peg_sprite_list[self.in_hand - 24] #start of dock is currently index -24?
        else:
            peg = self.gameboard.dock.peg_sprite_list[self.in_hand - 72]  #second row of dock starts at index - 48
        self.tile_list[self.num_dealt].position = peg.center_x, peg.center_y
        peg.occupy_peg(self.tile_list[self.num_dealt])

        # testing the get neighbor functions
        left_neighbor = self.gameboard.get_left_peg_neighbor(peg)
        right_neighbor = self.gameboard.get_right_peg_neighbor(peg)
        print(f"{peg} \n\tleft neighbor: {left_neighbor} \n\tright neighbor: {right_neighbor}")

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
        self.gameboard.draw()

        # Batch draw the grid sprites
        self.gameboard.all_pegs.draw()

        for peg in self.gameboard.all_pegs:
            arcade.draw_point(peg.center_x, peg.center_y, arcade.color.WHITE, size=5)

        # draw the tiles
        self.tile_list.draw()

        # draw the pass button
        self.pass_button.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

        self.button_press(x, y)


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        # revert pass button color
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.GREEN)

        if len(self.held_tiles) == 0:
            return

        peg, distance = arcade.get_closest_sprite(self.held_tiles[0], self.gameboard.all_pegs)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.tile:
            # For each held tile, move it to the pile we dropped on
            primary_tile = self.held_tiles[0]
            # Move tiles to proper position
            primary_tile.position = peg.center_x, peg.center_y

            # There is a tile on the peg
            p = arcade.get_sprites_at_point(primary_tile.position, self.gameboard.all_pegs)[-1]

            p.occupy_peg(primary_tile)

            # test get neighbor functions
            left_neighbor = self.gameboard.get_left_peg_neighbor(p)
            right_neighbor = self.gameboard.get_right_peg_neighbor(p)
            print(f"{p} \n\tleft neighbor: {left_neighbor} \n\tright neighbor: {right_neighbor}")

            # Success, don't reset position of tiles
            reset_position = False

        if arcade.check_for_collision(self.held_tiles[0], peg) and peg.tile:
            occupied_tile = peg.tile

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
        # print(f"{x}, {y}, {dx}, {dy}")

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


    def on_key_press(self, symbol: int, modifiers: int):
        # for now if user press' S reset tiles to O.G. Poss
        if symbol == arcade.key.S:
            for tile in self.tile_list:
                if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                    # look through all pegs to find where tile was sitting (before we move it)
                    # then set that peg to unocupied before we move it back.
                    # TODO: make this more efficient
                    for peg in self.gameboard.grid.peg_sprite_list:
                        if peg.center_x == tile.center_x and peg.center_y == tile.center_y:
                            peg.toggle_occupied()
                            break
                    tile.center_x = tile.start_of_turn_x
                    tile.center_y = tile.start_of_turn_y
                    # TODO: make this more efficient
                    # this is setting the place where the tile is moving to occupied.
                    for peg in self.gameboard.grid.peg_sprite_list:
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

    def button_press(self, x, y):

        moved_tiles = []
        left_empty = True
        right_empty = True

        valid_move = False
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            for tile in self.tile_list:
                if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                    moved_tiles.append(tile)

            # sort the moved tiles on x and y (in case of multiple moves in one turn)
            moved_tiles.sort(key=lambda t: (t.center_y, t.center_x))

            count = 0
            separator = Tile(f"tiles/EXAMPLE_00.png", scale=TILE_SCALE)
            moves = []
            current = []
            new_collection = Collection()
            new_collection.clear()
            temp_collection = Collection()
            temp_collections = []

            # to separate moves, insert an identifier in the list
            for tile in moved_tiles:
                if count == 0:
                    pass
                else: # need to account for if it is on the same line but not directly connected
                    if tile.center_y != moved_tiles[count - 1].center_y and moved_tiles[count - 1] != separator:
                        moved_tiles.insert(count, separator)
                count += 1

            # move separate moves into their own lists, contained in one mega list
            for tile in moved_tiles:
                if tile.__str__() == "EXAMPLE0":
                    moves.append(current)
                    current = []
                else:
                    current.append(tile)
            if current:
                moves.append(current)

            right_empty = False
            left_empty = False
            move_count = 0
            count = 0
            # add each seperate move into its own collection
            for move in moved_tiles:
                if move.__str__() == "EXAMPLE0":
                    #temp_collections.append(new_collection)
                    new_collection.clear()
                    move_count = 1
                else:
                    left_empty = False
                    right_empty = False
                    # check to see if left and right adjacent pegs are filled
                    for peg in self.gameboard.grid.peg_sprite_list:
                        if (peg.center_x - (
                                TILE_WIDTH + INNER_MARGIN)) == tile.center_x and peg.center_y == tile.center_y:
                            if peg.tile == None:
                                if new_collection.get_length() < 1:  # dont know why this isnt working
                                    left_empty = True

                        if (peg.center_x + (
                                TILE_WIDTH + INNER_MARGIN)) == tile.center_x and peg.center_y == tile.center_y:
                            if peg.tile == None:
                                right_empty = True

                    # if one neighboring peg is vacant, check which collection it belongs to and add the tile to it
                    # accounts for if the
                    if left_empty:
                        if move_count < len(moved_tiles):  # fix maybe
                            if len(self.collections) == 0:
                                new_collection.add(move, 0)
                    elif right_empty:
                        if move_count > 0:  # fix maybe
                            if len(self.collections) == 0:
                                new_collection.add(move, new_collection.get_length())

                    # if collections is not empty, check if the current tile is adjacent to any other collection
                    if len(self.collections) > 0:
                        for collections in self.collections:
                            near_bounds = collections.get_bounds()
                            if near_bounds[0] == tile.center_x - (TILE_WIDTH + INNER_MARGIN):
                                collections.add(tile)
                                print(tile)
                            elif near_bounds[1] == tile.center_x + (TILE_WIDTH + INNER_MARGIN):
                                collections.add(tile)
                                print(tile)
                try:
                    if moved_tiles[count + 1].__str__() == "EXAMPLE0":
                        temp_collections.append(new_collection)
                except(IndexError):
                    temp_collections.append(new_collection)
                    # elif len(move) != len(new_collection):
                move_count += 1
                count += 1

            print(temp_collections)
            for collection in temp_collections:
                for tile in collection.get_tiles():
                    print(tile)
                print("\n")

        """moved_tiles = []
        pos = [x, y]
        if self.pass_button.is_clicked(pos):
            self.pass_button.set_color(arcade.color.LINCOLN_GREEN)
            for tile in self.tile_list:
                if tile.start_of_turn_x != 0 and tile.start_of_turn_y != 0:
                    moved_tiles.append(tile)
            
        temp_collection = Collection()
        temp_collections = []
        for peg in self.gameboard.grid.peg_sprite_list:
            if peg.tile != None:
                if peg.tile in moved_tiles:
                    if peg.tile."""
