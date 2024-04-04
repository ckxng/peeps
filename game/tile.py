from game.container import container_trait
from game.location import Location


# @container_trait
class Tile(Location):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return " "
