from lib.base import BaseEntity
from lib.stat import StatType


class BaseMapEntity(BaseEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=y)
        self.stats[StatType.HEALTH].upgrade(499999)  # be sturdy
        self.stats[StatType.LIFETIME].immutable(True)
        self.stats[StatType.CAPACITY].immutable(True)
        self.stats[StatType.SPEED].immutable(True)
        self.stats[StatType.STRENGTH].immutable(True)
        self.stats[StatType.SHIELD].immutable(True)
        self.stats[StatType.ARMOR].immutable(True)

    def __str__(self):
        return " "

    def step(self):
        pass

    @staticmethod
    def is_buildable(self):
        return False
