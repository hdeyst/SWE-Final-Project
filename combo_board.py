import arcade
import gameboard

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

        # Convert the clicked mouse position into grid coordinates
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row >= ROW_COUNT or row < 0 or column >= COLUMN_COUNT or column < 0:
            # Simply return from this method since nothing needs updating
            return

        # Flip the color of the sprite
        if self.peg_sprites[row][column].color == arcade.color.CEIL:
            self.peg_sprites[row][column].color = arcade.color.LAVENDER_BLUE
        else:
            self.peg_sprites[row][column].color = arcade.color.CEIL


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