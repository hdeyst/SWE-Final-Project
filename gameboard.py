"""File holding Gameboard class"""
import arcade
from game_components import Grid, Cheatsheet
from utils import (COLUMN_COUNT, COLUMN_COUNT_DOCK, ROW_COUNT, ROW_COUNT_DOCK,
                   WINDOW_WIDTH, WINDOW_HEIGHT, OUTER_MARGIN, CHEATSHEET_BOTTOM,
                   CHEATSHEET_WIDTH, CHEATSHEET_HEIGHT, NUM_AI_PLAYERS)

class Gameboard:
    def __init__(self):
        self.grid = Grid("grid", COLUMN_COUNT, ROW_COUNT)
        self.user_dock = Grid("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)

        # a list of ai players hands - helpful for game loop maybe?
        self.ai_player_hands = []

        # create docks for each ai player
        for _ in range(NUM_AI_PLAYERS):
            self.ai_player_hands.append(
                Grid("ai_dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)
            )

        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)

        for user_dp in self.user_dock.peg_sprite_list:
            self.all_pegs.append(user_dp)

        for ai_ph in self.ai_player_hands:
            for dp in ai_ph.peg_sprite_list:
                self.all_pegs.append(dp)

        self.cheatsheet = Cheatsheet(
            left=OUTER_MARGIN,
            bottom=CHEATSHEET_BOTTOM,
            width=CHEATSHEET_WIDTH,
            height=CHEATSHEET_HEIGHT,
        )

        # create the logo
        self.texture = arcade.load_texture("./misc/rummikub.png", )
        self.logo_sprite = arcade.Sprite(self.texture, scale=.2)
        self.logo_sprite.center_y = WINDOW_HEIGHT - 25
        self.logo_sprite.center_x = WINDOW_WIDTH / 2

    def draw(self):
        self.grid.draw()
        self.user_dock.draw()

        arcade.draw_sprite(self.logo_sprite)

        self.cheatsheet.draw()

    def get_user_dock(self):
        return self.user_dock
