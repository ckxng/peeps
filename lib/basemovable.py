from typing import Dict, Optional

from lib.base import BaseEntity
from lib.globals import MOVABLES
from lib.stat import StatType


class BaseMovableEntity(BaseEntity):
    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def __init__(self, region: str, x: int, y: int, controller: Optional[any] = None):
        super().__init__(region=region, x=x, y=y)
        MOVABLES[self._id] = self
        self._controller = controller
        self._controller.add_movable(self)
        self.stats[StatType.HEALTH].upgrade(9)  # to 10
        self.stats[StatType.SPEED].upgrade(1)  # to 1
        self.stats[StatType.LIFETIME].upgrade(499)  # to 500

    def __del__(self):
        del MOVABLES[self._id]
        if self._controller is not None:
            self._controller.remove_movable(self)

    def __str__(self):
        return "&"

    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def controller(self, controller: Optional[any] = None):
        if controller is not None:
            self._controller = controller
        return self._controller

    def no_controller(self):
        self._controller = None

    def to_dict(self, show_all: bool = False, show_id: bool = False) -> Dict[str, any]:
        return super().to_dict(show_all=show_all, show_id=True)
