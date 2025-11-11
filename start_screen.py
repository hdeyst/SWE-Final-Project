import arcade
from utils import *
from gridboard import *
from game_view import GameView

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = arcade.color.MOONSTONE_BLUE
        self.start_button = Button(100, arcade.color.AIR_SUPERIORITY_BLUE,
                                 [WINDOW_WIDTH / 2,
                                  WINDOW_HEIGHT / 4],
                                 "Start Game")

    def on_draw(self):
        self.clear()
        if self.window.begin:
            self.start_button.draw()

    def on_hide_view(self):
        self.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        pos = [x, y]
        if self.start_button.is_clicked(pos):
            self.start_button.set_color(arcade.color.AIR_FORCE_BLUE)
            game_view = GameView()
            self.window.show_view(game_view)
