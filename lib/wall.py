from lib.basemap import BaseMapEntity
from lib.stat import StatType


class Wall(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=y)
        self.stats[StatType.HEALTH].immutable(False)
        self.stats[StatType.HEALTH].upgrade(49999)

    def __str__(self):
        return "#"
