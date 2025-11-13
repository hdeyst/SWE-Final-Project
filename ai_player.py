"""
AI-Player Class Description:

Properties:
    - hand (Tile_Collection)
    - is_turn (Boolean)
    - initial_melt (Boolean)
Functions:
    - "Check Hand"
    - "Check can lay down?"

"""
import arcade
from game_components import Dock

class Player:
    def __init__(self):
        # a player needs a dock ?
        self.dock = Dock()
