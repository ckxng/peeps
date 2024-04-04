from game.container import container_trait
from game.tile import Tile


@container_trait
class Box(Tile):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "U"
