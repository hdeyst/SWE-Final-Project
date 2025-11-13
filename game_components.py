"""
Defines 3 different types: Grid, Dock, and Button
- Grid creates the actual grid section of the game board,
  consisting of a variety of peg objects
- Dock extends Grid, and is the player's personal collection
  of tiles
- Button creates a custom button object to aid interactability
"""
import math
import arcade
from utils import GRID_WIDTH, GRID_HEIGHT, ROW_COUNT, COLUMN_COUNT, TILE_WIDTH, TILE_HEIGHT
from utils import INNER_MARGIN, OUTER_MARGIN, DOCK_OFFSET, WINDOW_WIDTH, ROW_COUNT_DOCK
from utils import COLUMN_COUNT_DOCK
from utils import KEY_BINDINGS, MINIMIZED_CS_WIDTH
from peg import Peg

class Grid:
    def __init__(self, placement, columns, rows):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.peg_sprite_list = arcade.SpriteList()
        self.peg_sprites = []

        self.placement = placement
        #print(f"filling {placement} w/ pegs!")
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
                peg.position = (x, y)
                #print(peg.position)

                # add peg to the various sprite lists
                self.peg_sprites[row].append(peg)
                self.peg_sprite_list.append(peg)
        #print(f"{placement} filled!: {len(self.peg_sprite_list)} pegs")

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




class Dock(Grid):
    def __init__(self, placement, columns, rows):
        super().__init__(placement, columns, rows)
        self.width = WINDOW_WIDTH
        self.placement = placement
        self.num_tiles = 0
        self.num_pegs = 0

    # default constructor for players
    def __init__(self):
        super().__init__(placement="dock", columns=COLUMN_COUNT_DOCK, rows=ROW_COUNT_DOCK)


    def draw(self):
        arcade.draw_rect_filled(
            arcade.LBWH(left=OUTER_MARGIN,
                        bottom=OUTER_MARGIN,
                        width=COLUMN_COUNT_DOCK * (TILE_WIDTH + INNER_MARGIN) + INNER_MARGIN,
                        height= ROW_COUNT_DOCK * (TILE_HEIGHT + INNER_MARGIN) + INNER_MARGIN),
            color=arcade.color.ROSY_BROWN
        )
        self.peg_sprite_list.draw()

    def get_sprites(self):
        return self.peg_sprite_list


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
