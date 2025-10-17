import arcade
from utils import *

class Peg(arcade.SpriteSolidColor):
    """A single peg sprite."""
    def __init__(self, width, height, color):
        super().__init__(width, height, color=color)

        # check for if a tile is already on a given peg
        self.occupied = False
        # POSSIBLE field for if a peg has a tile
        self.Tile = None

class Tile(arcade.Sprite):
    """A single tile sprite."""
    def __init__(self, filename, color, value, scale=1):
        super().__init__(filename, scale)
        self.tile_color = color
        self.value = value


class Grid():
    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []


        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN

                # create peg objects
                peg = Peg(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.CEIL)

                peg.center_x = x
                peg.center_y = y

                self.peg_sprite_list.append(peg)
                self.peg_sprites[row].append(peg)

    # helper function
    def convert_to_grid_coords(self, x, y):
        # Convert the clicked mouse position into grid coordinates
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        return column, row

    def get_nearest_peg(self, x, y):
        nearest_peg = arcade.get_sprites_at_point((x, y), self.peg_sprite_list)
        return nearest_peg

class GameView(arcade.View):
    """A game view."""
    def __init__(self):
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # create grid of gameboard
        self.grid = Grid()

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
                tile = Tile(f"tiles/{color}_{j + 1}.png", color, j + 1, scale=TILE_SCALE)

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

                peg.occupied = True
                # self.highlight_spot(peg.center_x, peg.center_y)

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

        nearest_peg = self.grid.get_nearest_peg(x, y)

        if len(tiles) > 0:
            primary_tile = tiles[-1]

            # All other cases, grab the tile we are clicking on
            self.held_tiles = [primary_tile]
            # Save the position
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_tiles[0])


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameView()
    game.build_deck(35, 55)

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()