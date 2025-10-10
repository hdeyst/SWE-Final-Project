"""
Solitaire clone.
"""
import arcade

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

NUM_TILES = 106
TILE_HEIGHT = SCREEN_HEIGHT // NUM_TILES
TILE_WIDTH = SCREEN_WIDTH // NUM_TILES

print(TILE_WIDTH, TILE_HEIGHT)


for i in range(10):
    pass

class Tile(arcade.Sprite):
    # scale can be used to alter the sizes of tiles eventually (?)
    def __init__(self, color, value, scale=1):
        self.color = color
        self.value = value

        # TODO: use quinn's pretty tiles
        self.image_file_name = f"/path/to/tile/imgs/{self.color}{self.value}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


t = Tile("blue", 1)

# set up window
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Testing Window")
background_color = arcade.color.PURPLE_TAUPE
arcade.set_background_color(background_color)

# start drawing
arcade.start_render()

# finish drawing
arcade.finish_render()

# keep output window open
arcade.run()
