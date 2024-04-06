from lib.basemap import BaseMapEntity
from lib.stat import StatType


# @container_trait
class Tile(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=y)
        self.stats[StatType.LIFETIME].immutable(True)
        self.stats[StatType.HEALTH].immutable(True)
        self.stats[StatType.SHIELD].immutable(True)
        self.stats[StatType.CAPACITY].immutable(True)
        self.stats[StatType.SPEED].immutable(True)
        self.stats[StatType.ARMOR].immutable(True)

    def __str__(self):
        return " "

    @staticmethod
    def is_buildable(self):
        return True
