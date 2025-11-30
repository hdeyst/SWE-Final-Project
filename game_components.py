"""
Defines 2 different types: Grid, and Button
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
- Button creates a custom button object to aid interactability
"""
import math
import arcade

from utils import GRID_WIDTH, GRID_HEIGHT, TILE_WIDTH, TILE_HEIGHT
from utils import INNER_MARGIN, OUTER_MARGIN, DOCK_OFFSET
from utils import KEY_BINDINGS, MINIMIZED_CS_WIDTH
from peg import Peg


class Grid:
    def __init__(self, placement, columns, rows):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.columns = columns
        self.rows = rows

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []

        self.tile_sprite_list = arcade.SpriteList()
        self.tile_sprites = []

        self.placement = placement

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
                if placement == "ai_dock":
                    peg.position = (-1, -1)
                else:
                    peg.position = (x, y)

                # add peg to the sprite lists
                self.peg_sprites[row].append(peg)
                self.peg_sprite_list.append(peg)

    def draw(self):
        # draw background boxes & their pegs depending on placement
        if self.placement == "dock":
            arcade.draw_rect_filled(
                arcade.LBWH(
                    left=OUTER_MARGIN,
                    bottom=OUTER_MARGIN,
                    width=self.columns * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                    height=self.rows * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN
                ),
                color=arcade.color.ROSY_BROWN
            )
            self.peg_sprite_list.draw()

        if self.placement == "grid":
            arcade.draw_rect_filled(
                arcade.LBWH(
                    left=OUTER_MARGIN,
                    bottom=DOCK_OFFSET + OUTER_MARGIN,
                    width=self.columns * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                    height=self.rows * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN
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

    def get_sprites(self):
        return self.peg_sprite_list

    def get_num_available_pegs(self):
        total = len(self.peg_sprite_list)
        for p in self.peg_sprite_list:
            if p.tile:
                total -= 1

    def get_num_occupied_pegs(self):
        count = 0
        for p in self.peg_sprite_list:
            if p.tile:
                count += 1
        return count



class Button():
    def __init__(self, radius, color, pos, text=''):
        self.color = color
        self.pressed_color = arcade.color.TROPICAL_RAIN_FOREST
        self.pos = pos
        self.text = text
        self.radius = radius
        self.pressed = False
        self.font_size = 12

        arcade.load_font("./misc/belwebold.otf")

    def draw(self):
        if not self.pressed:
            arcade.draw_circle_filled(self.pos[0], self.pos[1], self.radius, self.color)
        else:
            arcade.draw_circle_filled(self.pos[0], self.pos[1], self.radius, self.pressed_color)
        button_text = arcade.Text(
            self.text,
            self.pos[0],
            self.pos[1],
            arcade.color.BLACK,
            font_size=self.font_size,
            anchor_x="center",
            anchor_y="center",
            font_name="Belwe Bold",
        )
        button_text.draw()

    def is_clicked(self, pos):
        distance = math.sqrt((pos[0] - self.pos[0])**2 + (pos[1] - self.pos[1])**2)
        return distance <= self.radius

    def set_color(self, color):
        self.color = color


class ButtonRect():
    def __init__(self, width, height, pos, text=''):
        self.width = width
        self.height = height
        self.pos = pos

        self.color = arcade.color.HONOLULU_BLUE
        self.text = text
        self.pressed = False
        self.font_size = 12

        arcade.load_font("./misc/belwebold.otf")

    def draw(self):
        if not self.pressed:
            arcade.draw_rect_filled(
                arcade.XYWH(self.pos[0], self.pos[1], self.width, self.height), self.color)
        else:
            arcade.draw_rect_filled(
                arcade.XYWH(self.pos[0], self.pos[1], self.width, self.height),
                arcade.color.NAVY_BLUE
            )
        button_text = arcade.Text(
            self.text,
            self.pos[0],
            self.pos[1],
            arcade.color.BLACK,
            font_size=self.font_size,
            anchor_x="center",
            anchor_y="center",
            font_name="Belwe Bold",
        )
        button_text.draw()

    def is_clicked(self, pos):
        x_bounded = False
        y_bounded = False
        if (self.pos[0] - self.width/2 <= pos[0]) and (self.pos[0] + self.width/2 >= pos[0]):
            x_bounded = True
        if (self.pos[1] - self.height/2 <= pos[1]) and (self.pos[1] + self.height/2 >= pos[1]):
            y_bounded = True

        return x_bounded and y_bounded

    def set_color(self, color):
        self.color = color

    def press(self, pos):
        if self.is_clicked(pos):
            self.pressed = True
            self.set_color(arcade.color.NAVY_BLUE)


    def release(self):
        self.pressed = False
        self.set_color(arcade.color.HONOLULU_BLUE)



class Cheatsheet:
    def __init__(self, left, bottom, width, height):
        self.section_size = width / len(KEY_BINDINGS)
        self.show_keybinds = False
        self.font_size = 10

        # initialize dimensions
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

    def draw(self):
        if self.show_keybinds:
            self.expand_cheatsheet()
        else:
            self.minimize_cheatsheet()

    def expand_cheatsheet(self):
        # background rectangle
        arcade.draw_lbwh_rectangle_filled(
            left=self.left,
            bottom=self.bottom,
            width=self.width,
            height=self.height,
            color=arcade.color.AIR_FORCE_BLUE.replace(a=100),
        )

        # draw each key binding & its meaning
        text_offset_val = self.left + INNER_MARGIN
        for key in KEY_BINDINGS:
            txt = arcade.Text(
                f"{key}: {KEY_BINDINGS[key]}\t",
                x=text_offset_val,
                y=self.bottom + self.height / 2 - INNER_MARGIN,
                color=arcade.color.SMOKY_BLACK,
                font_size=self.font_size,
            )
            text_offset_val += self.section_size
            txt.draw()

    def minimize_cheatsheet(self):
        # background rectangle
        arcade.draw_lbwh_rectangle_filled(
            left=self.left,
            bottom=self.bottom,
            width=MINIMIZED_CS_WIDTH,
            height=self.height,
            color=arcade.color.AIR_FORCE_BLUE.replace(a=100)
        )

        # tell user how to view hotkey legend
        lbl = arcade.Text(
            "Press 'K' to toggle legend",
            x=self.left + INNER_MARGIN,
            y=self.bottom + self.height / 2 - INNER_MARGIN,
            color=arcade.color.SMOKY_BLACK,
            font_size=self.font_size,
        )
        lbl.draw()
