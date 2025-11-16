from utils import *
from game_components import Grid


class GameScratch:
    def __init__(self):
        self.grid = Grid("grid", COLUMN_COUNT, ROW_COUNT)
        self.player_hands = []

        # create docks for each player
        for _ in range(NUM_AI_PLAYERS):
            self.player_hands.append(
                Grid("dock", COLUMN_COUNT_DOCK, ROW_COUNT_DOCK)
            )

        self.all_pegs = arcade.SpriteList()
        for gp in self.grid.peg_sprite_list:
            self.all_pegs.append(gp)

        for ph in self.player_hands:
            for dp in ph.peg_sprite_list:
                self.all_pegs.append(dp)





if __name__ == "__main__":
    game = GameScratch()

    print(game.grid)
    for i, hand in enumerate(game.player_hands):
        print(f"player {i+1}")
        print(hand)

    for p in game.all_pegs:
        print(p)
    # print(game.player_hands)

