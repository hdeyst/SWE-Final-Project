import arcade
from utils import *
from peg import Peg

class Grid2:
    def __init__(self, placement, columns, rows):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []

        # dock inherits from grid, so don't hardcode "grid" here
        self.placement = placement

        # create 2D array of pegs
        for row in range(columns):
            # add nested lists to represent grid rows
            self.peg_sprites.append([])

            for col in range(rows):
                # get the center coords for each peg
                x = (col * (TILE_WIDTH + INNER_MARGIN) +
                     (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN)
                y = (row * (TILE_HEIGHT + INNER_MARGIN) +
                     (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN) + DOCK_OFFSET

                # create peg object
                peg = Peg(
                    TILE_WIDTH,
                    TILE_HEIGHT,
                    placement=placement,
                    row=row,
                    column=col
                )
                peg.position = (x, y)
                print(peg.position)

                # add peg to the various sprite lists
                self.peg_sprites[row].append(peg)
                self.peg_sprite_list.append(peg)

    def draw(self):
        arcade.draw_rect_filled(
            arcade.LBWH(left=OUTER_MARGIN,
                        bottom=DOCK_OFFSET + OUTER_MARGIN,
                        width=COLUMN_COUNT * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                        height=ROW_COUNT * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN
                        ),
            color=arcade.color.SHADOW_BLUE
        )
        self.peg_sprite_list.draw()

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
