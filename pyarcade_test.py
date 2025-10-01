"""
Tile Example with Arcade
"""

import arcade

# --- Window constants ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Tile Example"

# --- Tile constants ---
TILE_SCALE = 0.6
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE


class Tile(arcade.Sprite):
    """A single tile/card sprite."""
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

    def setup(self):
        """Set up the game here. Call this to restart."""
        # Add a single red9 tile
        tile = Tile("red9.png", TILE_SCALE)
        tile.center_x = WINDOW_WIDTH // 2
        tile.center_y = WINDOW_HEIGHT // 2
        self.tile_list.append(tile)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.tile_list.draw()

    def on_update(self, delta_time: float):
        """Game logic (not used yet)."""
        pass

    def on_key_press(self, key, key_modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            arcade.exit()


def main():
    """Main function."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
