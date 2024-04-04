from const.stat import StatType
from ent.base import BaseEntity


class Wall(BaseEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)
        self.stats[StatType.HEALTH].upgrade(499)
        self.stats[StatType.LIFETIME].immutable(True)  # don't degrade

    def __str__(self):
        return "#"
