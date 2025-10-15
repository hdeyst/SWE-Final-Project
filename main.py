"""
Basic Basic Game Board
"""
import arcade

# --- Tile constants ---
TILE_SCALE = .4
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE

# --- Grid constants ---
ROW_COUNT = 8
COLUMN_COUNT = 11
INNER_MARGIN = 5 # between cells in grid
OUTER_MARGIN = 30 # around the outside of the grid

# --- Screen constants ---
WINDOW_WIDTH = (TILE_WIDTH + INNER_MARGIN) * COLUMN_COUNT + OUTER_MARGIN * 2
WINDOW_HEIGHT = (TILE_HEIGHT + INNER_MARGIN) * ROW_COUNT + OUTER_MARGIN * 2
WINDOW_TITLE = "Rummikub Game Board!"

class Gameboard(arcade.View):

    def __init__(self):
        super().__init__()

        self.grid = []
        # TODO: in the future, it would be cool if maybe a grid element
        # was also a sprite, but an empty tile sprite? this might help w/
        # overlapping/snapping to place
        # also that way we can give them attributes- len, width (in case we
        # decide to scale stuff), center, etc
        for row in range(ROW_COUNT):
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)

        # Set the background window
        arcade.set_background_color(arcade.color.EMINENCE)

    def on_draw(self):
        """
        Draw the game board.
        """
        self.clear()

        # Draw grid by iterating through and checking values
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 1:
                    color = arcade.color.LAVENDER
                else:
                    color = arcade.color.NADESHIKO_PINK

                x = (INNER_MARGIN + TILE_WIDTH) * column + OUTER_MARGIN + TILE_WIDTH // 2
                y = (INNER_MARGIN + TILE_HEIGHT) * row + OUTER_MARGIN + TILE_HEIGHT // 2

                arcade.draw_rect_filled(arcade.rect.XYWH(x, y, TILE_WIDTH, TILE_HEIGHT), color)

    def on_mouse_press(self, x, y, button, modifiers):
        # Change the x/y screen coordinates to grid coordinates
        col, row = self.convert_coords(x, y)
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {col})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if ((row < ROW_COUNT and row >= 0) and
                (col < COLUMN_COUNT and col >= 0)):
            # Flip the location between 1 and 0.
            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            else:
                self.grid[row][col] = 0

    def convert_coords(self, x, y):
        # math:
        # get the clicked x value and subtract the outer margin value to make
        # sure you don't go over total window size.
        # floor divide that value by the size of the tile while accounting for
        # the margin. Do similar thing for y
        column = int((x - OUTER_MARGIN) // (TILE_WIDTH + INNER_MARGIN))
        row = int((y - OUTER_MARGIN) // (TILE_HEIGHT + INNER_MARGIN))

        return column, row


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = Gameboard()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()