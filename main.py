"""file to run game through"""
import arcade
from utils import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from game_view import GameView, StartView


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    game = GameView()

    start = StartView()
    # Show GameView on screen
    window.show_view(start)
    #window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
