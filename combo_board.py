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


class Peg(arcade.Sprite):
    """A single peg sprite."""
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """
        super().__init__()

        # Set the background color of the window
        self.background_color = arcade.color.ASH_GREY

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()
        self.grid_tile_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []
        self.grid_tiles = []

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            self.grid_tiles.append([])
            for column in range(COLUMN_COUNT):
                x = column * (TILE_WIDTH + INNER_MARGIN) + (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN
                y = row * (TILE_HEIGHT + INNER_MARGIN) + (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN

                peg = Peg("peg.png")
                sprite = arcade.SpriteSolidColor(TILE_WIDTH, TILE_HEIGHT, color=arcade.color.CEIL)

                peg.center_x = x
                peg.center_y = y
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

                self.grid_tile_list.append(peg)
                self.grid_tiles[row].append(peg)

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw the grid sprites
        self.grid_sprite_list.draw()
        self.grid_tile_list.draw()

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
        if row >= ROW_COUNT or column >= COLUMN_COUNT:
            # Simply return from this method since nothing needs updating
            return

        # Flip the color of the sprite
        if self.grid_sprites[row][column].color == arcade.color.CEIL:
            self.grid_sprites[row][column].color = arcade.color.LAVENDER_BLUE
        else:
            self.grid_sprites[row][column].color = arcade.color.CEIL


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()