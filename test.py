"""
Tile Example with Arcade
"""
import arcade
import utils
import gameboard


class Tile(arcade.Sprite):
    """A single tile sprite."""
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)

class Peg(arcade.Sprite):
    """A single peg sprite."""
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)


class GameView(arcade.View):
    """Main game view."""

    def __init__(self):
        super().__init__()

        # Background color
        self.background_color = arcade.color.BLUE_SAPPHIRE
        # Sprite list for tiles
        self.tile_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()

        self.held_tiles = None
        self.held_tiles_original_position = None

    def setup(self):
        """Set up the game here. Call this to restart."""
        self.held_tiles = []
        self.held_tiles_original_position = []

        board = gameboard.Gameboard()
        for i in board.pegs:
            peg = Peg("tiles/black_1.png", utils.TILE_SCALE)
            peg.center_x = i[0]
            peg.center_y = i[1]
            self.peg_list.append(peg)


        for i in range(4):
            for j in range(13):
                if i == 0: color = "cyan"
                elif i == 1: color = "red"
                elif i == 2: color = "yellow"
                else: color = "black"
                tile = Tile(f"tiles/{color}_{j + 1}.png", utils.TILE_SCALE)
                # Grid placement, lays all tiles out to see
                #tile.center_x = 0 + utils.TILE_WIDTH * (j + 1)
                #tile.center_y = utils.WINDOW_HEIGHT - ((i + 1) * utils.TILE_HEIGHT)

                # Stacked tile placement, places all tiles in the top left stacked on one another
                tile.center_x = 0 + utils.TILE_WIDTH
                tile.center_y = utils.WINDOW_HEIGHT - utils.TILE_HEIGHT
                self.tile_list.append(tile)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.tile_list.draw()
        self.peg_list.draw()

    def on_update(self, delta_time: float):
        """Game logic (not used yet)."""
        pass

    def on_key_press(self, key, key_modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.R:
            #TODO: find a way to reset the screen when the users presses "r"
            self.clear()


    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        tiles = arcade.get_sprites_at_point((x, y), self.tile_list)

        if len(tiles) > 0:
            primary_tile = tiles[-1]

            # All other cases, grab the tile we are clicking on
            self.held_tiles = [primary_tile]
            # Save the position
            self.held_tiles_original_position = [self.held_tiles[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_tiles[0])

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        for tile in self.held_tiles:
            tile.center_x += dx
            tile.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        if len(self.held_tiles) == 0:
            return
        self.held_tiles = []

    def pull_to_top(self, tile: arcade.Sprite):
        """ Pull tile to top of rendering order (last to render, looks on-top) """
        self.tile_list.remove(tile)
        self.tile_list.append(tile)

def main():
    """Main function."""
    window = arcade.Window(utils.WINDOW_WIDTH, utils.WINDOW_HEIGHT, utils.WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
