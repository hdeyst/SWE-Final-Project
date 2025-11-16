from utils import *
from peg import *
# from game_components import *

class Grid2:
    def __init__(self, placement, columns, rows):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.placement = placement

        self.peg_sprites = []

        # create 2D array of pegs
        for row in range(rows):
            # add nested lists to represent grid rows
            self.peg_sprites.append([])

            for col in range(columns):
                # get the center coords for each peg
                x = (col * (TILE_WIDTH + INNER_MARGIN) +
                     (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN)
                y = (row * (TILE_HEIGHT + INNER_MARGIN) +
                     (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN)

                # move grid up to make space for dock
                if placement == "grid":
                    y += DOCK_OFFSET

                # create peg object
                peg = Peg(
                    TILE_WIDTH,
                    TILE_HEIGHT,
                    placement=self.placement,
                    position=[row, col]
                )
                peg.position = (x, y)
                # print(peg.position)

                # add peg to the various sprite lists
                self.peg_sprites[row].append(peg)

    def __str__(self):
        representation = ""
        for row in self.peg_sprites:
            for peg in row:
                if peg.tile:
                    representation += "[t] "
                else:
                    representation += "[ ] "
            representation += "\n"
        return representation



if __name__ == "__main__":
    g = Grid2("grid", COLUMN_COUNT, ROW_COUNT)
    d = Grid2("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)

    print(g)
    print(d)

