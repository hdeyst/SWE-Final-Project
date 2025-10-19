import arcade
import utils


class Tile(arcade.Sprite):
    """A single tile sprite."""
    color = ""
    number = 0
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        # tile = Tile(f"tiles/{color}_{j + 1}.png", utils.TILE_SCALE)
        split = filename.split("_")
        color_split = split[0].split("tiles/")
        self.color = color_split[1]

        number_split = split[1].split(".")
        self.number = int(number_split[0])

if __name__ == "__main__":
    tile = Tile(f"../tiles/black_1.png", utils.TILE_SCALE)

    print(tile.number)
