from lib.base import BaseEntity
from lib.basecontroller import BaseControllerEntity
from lib.stat import StatType


class BaseMovableEntity(BaseEntity):
    def __init__(self, region: str, x: int, y: int, controller: BaseControllerEntity = None):
        super().__init__(region=region, x=x, y=y)
        self._controller = controller
        self.stats[StatType.HEALTH].upgrade(9)  # to 10
        self.stats[StatType.SPEED].upgrade(1)  # to 1
        self.stats[StatType.LIFETIME].upgrade(499)  # to 500

    def __str__(self):
        return "&"
