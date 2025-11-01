import arcade
from utils import *
from rewrite_grid import Grid2
from gridboard import Grid, Dock

class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ASH_GREY
        self.grid = Grid(COLUMN_COUNT, ROW_COUNT)
        self.dock = Dock("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)
        print(self.grid)
        print()
        print(self.dock)

    def on_draw(self):
        self.clear()
        self.grid.draw()
        self.dock.draw()

    # def on_mouse_motion(self, x, y, dx, dy):
    #     pegs = arcade.get_sprites_at_point((x, y), self.grid.peg_sprite_list)
    #     for peg in pegs:
    #         peg.highlight()
    #         print(peg)


def main2():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = Game()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main2()