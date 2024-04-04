from const.resource import ResourceType
from const.stat import StatType
from ent.base import BaseEntity


class Item(BaseEntity):
    def __init__(self, region: str, x: int, y: int, resource: ResourceType, qty=1):
        super().__init__(region=region, x=x, y=x)
        self.type = resource

        # quantity of a stack of items is tracked by its lifetime stat
        # the stack disappears when lifetime naturally decreases to zero
        self.stats[StatType.LIFETIME].no_max()
        self.stats[StatType.LIFETIME].value(qty)
        self.stats[StatType.LIFETIME].natural_step(1)

    def __str__(self):
        return "."
