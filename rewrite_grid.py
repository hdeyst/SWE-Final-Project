import arcade
from utils import *
from rewrite_peg import Peg2

class Grid2:
    def __init__(self, left, right, bottom, top):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()

        # these are the same
        self.peg_sprites = []
        self.peg_2D_array = []

        # create 2D array of pegs
        for row in range(ROW_COUNT):
            # add nested lists to represent grid rows
            self.peg_sprites.append([])
            self.peg_2D_array.append([])

            for col in range(COLUMN_COUNT):
                # get the center coords for each peg
                x = (col * (TILE_WIDTH + INNER_MARGIN) +
                     (TILE_WIDTH / 2 + INNER_MARGIN) + OUTER_MARGIN)
                y = (row * (TILE_HEIGHT + INNER_MARGIN) +
                    (TILE_HEIGHT / 2 + INNER_MARGIN) + OUTER_MARGIN) + DOCK_OFFSET

                peg = Peg2(
                        TILE_WIDTH,
                        TILE_HEIGHT,
                        placement="grid",
                        row=row,
                        column=col
                    )
                peg.position = (x, y)
                print(peg.position)
                self.peg_2D_array[row].append(peg)
                self.peg_sprites[row].append(peg)
                self.peg_sprite_list.append(peg)


    def __str__(self):
        representation = ""
        for row in self.peg_2D_array:
            for peg in row:
                if peg.tile:
                    representation += "[t] "
                else:
                    representation += "[ ] "
            representation += "\n"
        return representation

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


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.grid = Grid2(
            left=OUTER_MARGIN,
            right=WINDOW_WIDTH - OUTER_MARGIN + INNER_MARGIN,
            bottom=DOCK_OFFSET + OUTER_MARGIN,
            top=WINDOW_HEIGHT - OUTER_MARGIN + INNER_MARGIN
        )
        print(self.grid)
    def on_draw(self):
        self.clear()
        self.grid.draw()



# print(g)



window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
game = Game()
window.show_view(game)
arcade.run()
