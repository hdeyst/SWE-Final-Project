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
from utils import COLUMN_COUNT_DOCK, ROW_COUNT_DOCK


class Player:
    def __init__(self):
        # a player needs a dock ?
        self.user_dock = Dock(placement="dock", columns=COLUMN_COUNT_DOCK, rows=ROW_COUNT_DOCK)

        # get the number of slots the player has in their dock
        self.num_dock_pegs = COLUMN_COUNT_DOCK * ROW_COUNT_DOCK
        self.held_tiles = []