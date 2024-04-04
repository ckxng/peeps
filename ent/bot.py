from const.stat import StatType
from ent.base import BaseEntity
from game.container import container_trait


@container_trait
class Bot(BaseEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)
        self.stats[StatType.HEALTH].upgrade(9)  # to 10
        self.stats[StatType.SPEED].upgrade(1)  # to 1
        self.stats[StatType.LIFETIME].upgrade(499)  # to 500

    def __str__(self):
        return "&"
