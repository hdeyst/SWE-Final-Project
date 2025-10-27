import arcade
import utils


class Tile(arcade.Sprite):
    """A single tile sprite."""
    color = ""
    number = 0
    start_of_turn_x = 0
    start_of_turn_y = 0
    in_dock = True
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        # tile = Tile(f"tiles/{color}_{j + 1}.png", utils.TILE_SCALE)
        split = filename.split("_")
        color_split = split[0].split("tiles/")
        self.color = color_split[1]

        number_split = split[1].split(".")
        self.number = int(number_split[0])

    def __str__(self):
        return f"{self.color}{self.number}"

    def set_start_of_turn_pos(self, x, y):
        self.start_of_turn_x = x
        self.start_of_turn_y = y

if __name__ == "__main__":
    tile = Tile(f"../tiles/black_1.png", utils.TILE_SCALE)

    print(tile)
