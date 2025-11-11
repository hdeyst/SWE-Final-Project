import arcade
from utils import *

class Cheatsheet(arcade.Section):
    def __init__(self, left, bottom, width, height, name, accept_keyboard_keys={arcade.key.K}):
        super().__init__(left, bottom, width, height, name=name)
        self.section_size = width / (len(KEY_BINDINGS) + 1)
        self.show_keybinds = True
        print(f"left: {left}, bottom: {bottom}, width: {width}, height: {height}")

    def on_draw(self):
        if self.show_keybinds:
            arcade.draw_lbwh_rectangle_filled(
                left=self.left,
                bottom=self.bottom,
                width=self.width,
                height=self.height,
                color=arcade.color.AIR_SUPERIORITY_BLUE.replace(a=150)
            )
            lbl = arcade.Text(
                "Hotkeys: ",
                x=self.left + INNER_MARGIN,
                y= self.bottom + self.height / 2 - INNER_MARGIN,
                color=arcade.color.BLACK,
            )
            lbl.draw()
            text_offset_val = self.left + self.section_size + INNER_MARGIN
            for key in KEY_BINDINGS:
                txt = arcade.Text(
                    f"{key}: {KEY_BINDINGS[key]}\t",
                    x=text_offset_val,
                    y=self.bottom + self.height/2 - INNER_MARGIN,
                    color=arcade.color.BLACK,
                )
                text_offset_val += self.section_size
                txt.draw()
        else:
            arcade.draw_lbwh_rectangle_filled(
                left=self.left,
                bottom=self.bottom,
                width=MINIMIZED_CS_WIDTH,
                height=self.height,
                color=arcade.color.AIR_SUPERIORITY_BLUE.replace(a=150)
            )
            lbl = arcade.Text(
                "Press 'K' to toggle cheatsheet",
                x=self.left + INNER_MARGIN,
                y=self.bottom + self.height / 2 - INNER_MARGIN,
                color=arcade.color.BLACK,
            )
            lbl.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(f"{x},{y},{button},{modifiers}")
        print("clicked in cheatsheet")

    # press K to toggle key binding cheat sheet
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.K:
            self.show_keybinds = not self.show_keybinds
        else:
            # let the game_view handle all other inputs
            self.view.on_key_press(symbol, modifiers)