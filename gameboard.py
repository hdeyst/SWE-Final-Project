
import utils
class Gameboard:
    def __init__(self):
        self.width = utils.WINDOW_WIDTH
        self.height = utils.WINDOW_HEIGHT
        #  pegs = [(x, y), (x1, y1)]
        # 8 x 14 board

        coord_map = []
        rows, cols = 10, 18
        for row in range(rows):
            for col in range(cols):
                x_coord = utils.TILE_WIDTH / 2 + col * utils.TILE_WIDTH
                y_coord = self.height - (utils.TILE_HEIGHT / 2 + row * (utils.TILE_HEIGHT + utils.PEG_SPACING_Y))
                coord_map.append([x_coord, y_coord])
        self.pegs = coord_map


