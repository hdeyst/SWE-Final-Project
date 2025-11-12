import arcade
from utils import KEY_BINDINGS, INNER_MARGIN, MINIMIZED_CS_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH


class Cheatsheet:
    def __init__(self, left, bottom, width, height):
        self.section_size = width / (len(KEY_BINDINGS) + 1)
        self.show_keybinds = False
        self.font_size = 10
        self.name = "Cheatsheet"

        # initialize dimensions
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

    def draw(self):
        if self.show_keybinds:
            arcade.draw_lbwh_rectangle_filled(
                left=self.left,
                bottom=self.bottom,
                width=self.width,
                height=self.height,
                color=arcade.color.AIR_FORCE_BLUE.replace(a=100),
            )
            lbl = arcade.Text(
                "Hotkey Cheatsheet: ",
                x=self.left + INNER_MARGIN,
                y= self.bottom + self.height / 2 - INNER_MARGIN,
                color=arcade.color.BLACK,
                font_size=self.font_size,
            )
            lbl.draw()
            text_offset_val = self.left + self.section_size + INNER_MARGIN*2
            for key in KEY_BINDINGS:
                txt = arcade.Text(
                    f"{key}: {KEY_BINDINGS[key]}\t",
                    x=text_offset_val,
                    y=self.bottom + self.height/2 - INNER_MARGIN,
                    color=arcade.color.BLACK,
                    font_size=self.font_size,
                )
                text_offset_val += self.section_size
                txt.draw()
        else:
            arcade.draw_lbwh_rectangle_filled(
                left=self.left,
                bottom=self.bottom,
                width=MINIMIZED_CS_WIDTH,
                height=self.height,
                color=arcade.color.AIR_FORCE_BLUE.replace(a=100)
            )
            lbl = arcade.Text(
                "Press 'K' to toggle cheatsheet",
                x=self.left + INNER_MARGIN,
                y=self.bottom + self.height / 2 - INNER_MARGIN,
                color=arcade.color.BLACK,
                font_size=self.font_size,
            )
            lbl.draw()