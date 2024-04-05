from uuid import uuid4

from game.tile import Tile


class Spawn(Tile):
    def __init__(self):
        super().__init__()
        self._id = str(uuid4())
        # TODO register spawns with a global lookup so they can accept commands
        # TODO assign player ownership

    def __str__(self):
        return "s"
