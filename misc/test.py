"""
Tile Example with Arcade
"""
import arcade
import utils
from classes import Gameboard

# --- Window constants ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Tile Example"

# --- Tile constants ---
TILE_SCALE = 0.6
TILE_WIDTH = 140 * TILE_SCALE
TILE_HEIGHT = 190 * TILE_SCALE
TILE_COLORS = ["cyan", "red", "yellow", "black"]


class Tile(arcade.Sprite):
    """A single tile sprite."""
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        #tile = Tile(f"tiles/{color}_{j + 1}.png", utils.TILE_SCALE)
        split = filename.split("_")
        color_split = split[0].split("/")
        color = color_split[1]

        number_split = split[1].split(".")
        number = number_split[1]


class Collection:
    def __init__(self, tile): #assuming a collection will be created whenever a tile is added to the board alone
        self.tiles = [tile]
        self.isSet = True

    def add(self, tile, index):
        self.tiles.insert(index, tile) #ensuring the list will be in the same order as on the board
                                       #could use positions to determine order if we want to make Tile less abstract?

    def remove(self, item):
        self.tiles.remove(item)

    def getValue(self):
        sum = 0
        for tile in self.tiles:
            sum += tile.number
        return sum

    def set(self): #3-4 same number, different colors
        self.isSet = True
        if len(self.tiles) == 3:
            if self.tiles[0].color == self.tiles[1].color or self.tiles[0].color == self.tiles[2].color or self.tiles[1].color == self.tiles[2].color:
                return False
        elif len(self.tiles) == 4:
            if self.tiles[0].color == self.tiles[1].color or self.tiles[0].color == self.tiles[2].color or self.tiles[0].color == self.tiles[3].color\
                    or self.tiles[1].color == self.tiles[2].color or self.tiles[1].color == self.tiles[3].color or self.tiles[2].color == self.tiles[3].color:
                return False
        else: #incorrect length for set
            return False
        for tile in self.tiles:
            if tile.number != self.tiles[0].number:
                return False
        return self.isSet

    def run(self): #3+ same color, increasing numbers
        if len(self.tiles) < 3:
            return False
        for index in range(len(self.tiles)):
            if self.tiles[index].color != self.tiles[0].color:
                return False
            if index > 0 and not self.tiles[index - 1].number < self.tiles[index].number:
                return False
        return True



    def isValid(self):
        if self.set() == True or self.run() == True:
            return True
        return False


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
            peg = Peg("peg.png", utils.TILE_SCALE)
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
            self.__init__()
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

        peg, distance = arcade.get_closest_sprite(self.held_tiles[0], self.peg_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_tiles[0], peg):
            # For each held tile, move it to the pile we dropped on
            for i, dropped_card in enumerate(self.held_tiles):
                # Move tiles to proper position
                dropped_card.position = peg.center_x, peg.center_y
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

def main():
    """Main function."""
    window = arcade.Window(utils.WINDOW_WIDTH, utils.WINDOW_HEIGHT, utils.WINDOW_TITLE)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    #main()

    r0 = Tile(0, "red")
    b0 = Tile(0, "blue")
    g0 = Tile(0, "green")
    o0 = Tile(0, "orange")
    r1 = Tile(1, "red")
    r2 = Tile(2, "red")
    r3 = Tile(3, "red")

    group0 = Collection(r0) #all 0s, 3 different colors
    group0.add(g0, 1)
    group0.add(b0, 2)
    group0.add(o0, 3)

    group1 = Collection(r0)  #all 0s, 4 different colors
    group1.add(g0, 1)
    group1.add(b0, 2)
    group1.add(o0, 3)

    group2 = Collection(r0)  #all reds, [0,1,2,3]
    group2.add(r1, 1)
    group2.add(r2, 2)
    group2.add(r3, 3)


    print(group0.isValid())
    print(group1.isValid())
    print(group2.isValid())

