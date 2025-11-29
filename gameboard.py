"""File holding Gameboard class"""
import arcade
from game_components import Grid, Cheatsheet, Button, ButtonRect
from utils import (COLUMN_COUNT, COLUMN_COUNT_DOCK, ROW_COUNT, ROW_COUNT_DOCK,
                   WINDOW_WIDTH, WINDOW_HEIGHT, OUTER_MARGIN, CHEATSHEET_BOTTOM,
                   CHEATSHEET_WIDTH, CHEATSHEET_HEIGHT, PASS_BUTTON_POS, BUTTON_X, BUTTON_Y, END_TURN_BUTTON_POS)

class Gameboard:
    def __init__(self):
        self.grid = Grid("grid", COLUMN_COUNT, ROW_COUNT)
        self.user_dock = Grid("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)

        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)

        for user_dp in self.user_dock.peg_sprite_list:
            self.all_pegs.append(user_dp)

        self.cheatsheet = Cheatsheet(
            left=OUTER_MARGIN,
            bottom=CHEATSHEET_BOTTOM,
            width=CHEATSHEET_WIDTH,
            height=CHEATSHEET_HEIGHT,
        )

        # create the logo
        self.texture = arcade.load_texture("misc/rummikub.png", )
        self.logo_sprite = arcade.Sprite(self.texture, scale=.2)
        self.logo_sprite.center_y = WINDOW_HEIGHT - 25
        self.logo_sprite.center_x = WINDOW_WIDTH / 2

        # initialize buttons
        self.pass_button = Button(50, arcade.color.GREEN, PASS_BUTTON_POS, "")
        self.button_text = (
            arcade.Text("Pass", BUTTON_X, BUTTON_Y, arcade.color.BLACK, 16,
                        anchor_x="center", anchor_y="center", font_name="Belwe Bold")
        )
        self.end_turn_button = (
            ButtonRect(125, 40, END_TURN_BUTTON_POS, "Restart Game")
        )


    def draw(self):
        self.grid.draw()
        self.user_dock.draw()

        arcade.draw_sprite(self.logo_sprite)

        self.cheatsheet.draw()

        # draw the pass button
        self.pass_button.draw()
        self.button_text.draw()
        self.end_turn_button.draw()

    def get_user_dock(self):
        return self.user_dock
