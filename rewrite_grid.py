import arcade
from utils import *
from peg import Peg

class Grid2:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []

        self.peg_2D_array = []

        # create 2D array of pegs
        for row in range(ROW_COUNT):
            self.peg_2D_array.append([])
            print("[ ] " * COLUMN_COUNT)
            for col in range(COLUMN_COUNT):
                self.peg_2D_array[row].append(Peg(row, col))


    def draw(self):
        # back of the board
        arcade.draw_rect_filled(
            arcade.LRBT(
                left=self.left,
                right=self.right,
                bottom=self.bottom,
                top=self.top
            ),
            color=arcade.color.SHADOW_BLUE
        )

g = Grid2(
    left=OUTER_MARGIN,
    right=WINDOW_WIDTH - OUTER_MARGIN,
    bottom=DOCK_OFFSET + OUTER_MARGIN,
    top=WINDOW_HEIGHT - OUTER_MARGIN
)

window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
g.draw()
arcade.run()
