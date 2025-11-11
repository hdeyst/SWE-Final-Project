from utils import *
from arcade.gui import *
import arcade.gui

class StartScreen(arcade.View):
    def __init__(self, main_view):
        super().__init__(main_view)

        self.background = arcade.color.MOONSTONE_BLUE
        # Create a anchor layout, which can be used to position widgets on screen
        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(UIAnchorLayout())

        start_text = UITextArea(
            text="THESE ARE THE INSTRUCTIONS FOR RUMMIKUB !",
            text_color=arcade.color.ANTIQUE_WHITE,
            font_size=14,
        )
        start_text.with_border(color=arcade.color.ASH_GREY)
        start_text.with_background(color=arcade.color.MOONSTONE_BLUE.replace(a=150))
        start_text.with_padding(left=5)
        self.main_view = main_view


    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.color.MOONSTONE_BLUE)

        # Enable the UIManager when the view is shown.
        self.manager.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_draw(self):
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the manager.
        self.manager.draw()
