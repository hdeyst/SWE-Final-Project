import arcade
from classes.gridboard import *
from classes.Tile import Tile

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # create grid of gameboard
        self.grid = Grid()
        self.dock = Dock(self.grid)

        # create list of tile sprites (which will use quinn's tiles)
        self.tile_list = arcade.SpriteList()

        self.held_tiles = None
        self.held_tiles_original_position = None

    # creates all possible tiles and puts them in a deck
    def build_deck(self, deck_x_pos, deck_y_pos):
        self.held_tiles = []
        self.held_tiles_original_position = []

        for color in COLORS:
            for j in range(13):
                tile = Tile(f"tiles/{color}_{j + 1}.png", scale=TILE_SCALE)

                # Stacked tile placement, places all tiles in the top left stacked on one another
                tile.center_x = deck_x_pos
                tile.center_y = deck_y_pos
                self.tile_list.append(tile)


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


    def on_mouse_press(self, x, y, button, modifiers):
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

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

            # Success, don't reset position of tiles
            reset_position = False

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset each tile's position
            # to its original spot.
            for tile_index, card in enumerate(self.held_tiles):
                card.position = self.held_tiles_original_position[tile_index]

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

        if len(tiles) > 0:
            primary_tile = tiles[-1]

            # All other cases, grab the tile we are clicking on
            self.held_tiles = [primary_tile]
            # Save the position
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_tiles[0])

            # mark the peg as available again
            nearest_peg = self.grid.get_nearest_peg(self.held_tiles[0])
            if nearest_peg.occupied:
                nearest_peg.toggle_occupied()