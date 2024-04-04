from game.tile import Tile


class Source(Tile):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "*"
