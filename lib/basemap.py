from lib.base import BaseEntity
from lib.stat import StatType


class BaseMapEntity(BaseEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)
        self.stats[StatType.HEALTH].upgrade(499999)  # be sturdy
        self.stats[StatType.LIFETIME].immutable(True)  # don't degrade

    def __str__(self):
        return " "

    def step(self):
        pass

    @staticmethod
    def is_buildable(self):
        return False

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
        }
