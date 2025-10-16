import arcade

# --- Tile constants ---
TILE_SCALE = .4
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE

# --- Grid constants ---
ROW_COUNT = 8
COLUMN_COUNT = 12
INNER_MARGIN = 5 # between cells in grid
OUTER_MARGIN = 50 # around the outside of the grid

# --- Screen constants ---
WINDOW_WIDTH = (TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT + OUTER_MARGIN * 2
WINDOW_HEIGHT = (TILE_HEIGHT + INNER_MARGIN) * ROW_COUNT + OUTER_MARGIN * 2
WINDOW_TITLE = "Rummikub Game Board!"

class Tile(arcade.Sprite):
    """A single tile sprite."""
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)

class GameView(arcade.View):
    """
    Main application class.
    """
    # TODO: convert this into a gameboard class
    # TODO: snap tiles to peg center
    # TODO: organize code into nicer functions

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = [] # 2D grid w/ same sprite objects as in peg_sprite_list

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.peg_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN

                sprite = arcade.SpriteSolidColor(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.CEIL)

                sprite.center_x = x
                sprite.center_y = y
                # add field for if there is a tile on the specified square
                sprite.occupied = False

                self.peg_sprite_list.append(sprite)
                self.peg_sprites[row].append(sprite)

        # create list of tile sprites (which will use quinn's tiles)
        self.tile_list = arcade.SpriteList()

        self.held_tiles = None
        self.held_tiles_original_position = None


    def setup(self):
        """Set up the game here. Call this to restart."""
        self.held_tiles = []
        self.held_tiles_original_position = []

        for i in range(4):
            for j in range(13):
                if i == 0:
                    color = "cyan"
                elif i == 1:
                    color = "red"
                elif i == 2:
                    color = "yellow"
                else:
                    color = "black"
                tile = Tile(f"tiles/{color}_{j + 1}.png", TILE_SCALE)

                # Stacked tile placement, places all tiles in the top left stacked on one another
                tile.center_x = 0 + TILE_WIDTH
                tile.center_y = WINDOW_HEIGHT - TILE_HEIGHT
                self.tile_list.append(tile)


    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw the grid sprites
        self.peg_sprite_list.draw()

        # draw the center points of each grid square
        for s in self.peg_sprite_list:
            arcade.draw_point(s.center_x, s.center_y, arcade.color.WHITE, size=5)

        # draw the tiles
        self.tile_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # get any tiles that might be selected
        self.pick_up_tile(x, y)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        for tile in self.held_tiles:
            tile.center_x += dx
            tile.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        if len(self.held_tiles) == 0:
            return

        peg, distance = arcade.get_closest_sprite(self.held_tiles[0], self.peg_sprite_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg) and not peg.occupied:
            # For each held tile, move it to the pile we dropped on
            for i, dropped_card in enumerate(self.held_tiles):
                # Move tiles to proper position
                dropped_card.position = peg.center_x, peg.center_y
                # TODO: mark that peg as filled
                #  (right now just changing its color)
                peg.occupied = True
                self.highlight_spot(peg.center_x, peg.center_y)

            # Success, don't reset position of tiles
            reset_position = False

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset each tile's position
            # to its original spot.
            for tile_index, card in enumerate(self.held_tiles):
                card.position = self.held_tiles_original_position[tile_index]


        self.held_tiles = []

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

            # if the tile was on the board, toggle the background color of square
            # self.highlight_spot(x, y)
            # peg = arcade.get_sprites_at_point((x, y), self.peg_sprite_list)
            # peg.occupied = True

    # function to highlight a grid position based on given (x, y) coords
    def highlight_spot(self, x, y):
        column, row = self.mouse_coords_to_grid(x, y)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # check if user clicked in the grid or in the margins
        if row >= ROW_COUNT or row < 0 or column >= COLUMN_COUNT or column < 0:
            # nothing needs to happen
            return

        # Flip the color of the sprite
        if self.peg_sprites[row][column].color == arcade.color.CEIL:
            self.peg_sprites[row][column].color = arcade.color.LAVENDER_BLUE
        else:
            self.peg_sprites[row][column].color = arcade.color.CEIL

    def mouse_coords_to_grid(self, x, y):
        # Convert the clicked mouse position into grid coordinates
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        return column, row


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()