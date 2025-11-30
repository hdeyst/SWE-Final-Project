from tile import Tile
from collection import Collection
from utils import TILE_SCALE

def test_runs():
    red2 = Tile("tiles/red_2.png", scale=TILE_SCALE)
    red3 = Tile("tiles/red_3.png", scale=TILE_SCALE)
    red4 = Tile("tiles/red_4.png", scale=TILE_SCALE)
    wild = Tile("tiles/red_wild.png", scale=TILE_SCALE)
    yellow2 = Tile("tiles/yellow_2.png", scale=TILE_SCALE)
    yellow3 = Tile("tiles/yellow_3.png", scale=TILE_SCALE)
    black2 = Tile("tiles/black_2.png", scale=TILE_SCALE)
    black5 = Tile("tiles/black_5.png", scale=TILE_SCALE)

    # testing sets
    wrong1 = Collection()
    wrong1.add(yellow2)
    wrong1.add(yellow3)

    wrong2 = Collection()
    wrong2.add(black2)
    wrong2.add(black5)

    wrong3 = Collection()
    wrong3.add(black2)
    wrong3.add(wild)
    wrong3.add(black5)

    wrong4 = Collection()
    wrong4.add(black2)
    wrong4.add(black5)
    wrong4.add(wild)

    right1 = Collection()
    right1.add(yellow2)
    right1.add(yellow3)
    right1.add(wild)

    right2 = Collection()
    right2.add(red2)
    right2.add(red3)
    right2.add(red4)

    run_tests = [wrong1, wrong2, wrong3, wrong4, right1, right2]
    for test in run_tests:
        print(f"{test}: {test.run()}")


def test_sets():
    red2 = Tile("tiles/red_2.png", scale=TILE_SCALE)
    red3 = Tile("tiles/red_3.png", scale=TILE_SCALE)
    red4 = Tile("tiles/red_4.png", scale=TILE_SCALE)
    wild = Tile("tiles/red_wild.png", scale=TILE_SCALE)
    yellow2 = Tile("tiles/yellow_2.png", scale=TILE_SCALE)
    black2 = Tile("tiles/black_2.png", scale=TILE_SCALE)

    # testing sets
    wrong1 = Collection()
    wrong1.add(yellow2)
    wrong1.add(red2)

    wrong2 = Collection()
    wrong2.add(red2)
    wrong2.add(red3)
    wrong2.add(red4)

    wrong3 = Collection()
    wrong3.add(black2)
    wrong3.add(wild)

    wrong4 = Collection()
    wrong4.add(black2)
    wrong4.add(red4)
    wrong4.add(wild)

    wrong5 = Collection()
    wrong5.add(black2)
    wrong5.add(wild)
    wrong5.add(red4)

    right1 = Collection()
    right1.add(yellow2)
    right1.add(red2)
    right1.add(wild)

    right2 = Collection()
    right2.add(red2)
    right2.add(yellow2)
    right2.add(black2)

    set_tests = [wrong1, wrong2, wrong3, wrong4, wrong5, right1, right2]
    for test in set_tests:
        print(f"{test}: {test.set()}")


if __name__ == "__main__":
    collection = Collection()
    print("Sets: 5 false, 2 true")
    test_sets()
