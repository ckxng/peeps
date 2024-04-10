from enum import Enum
from typing import Dict, Optional

from lib.base import BaseEntity
from lib.globals import MOVABLES, REGIONS
from lib.stat import StatType


class MovableActionType(Enum):
    MOVE = "move"


class BaseMovableEntity(BaseEntity):
    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def __init__(self, region: str, x: int, y: int, controller: Optional[any] = None):
        super().__init__(region=region, x=x, y=y)

        MOVABLES[self._id] = self
        self._controller = controller
        if self._controller is not None:
            self._controller.add_structure(self)

        self.stats[StatType.HEALTH].upgrade(9)  # to 10
        self.stats[StatType.SPEED].upgrade(1)  # to 1
        self.stats[StatType.LIFETIME].upgrade(499)  # to 500

        self._actions: Dict[MovableActionType, Dict[str, any]] = {}

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

    def add_action(self, action: MovableActionType, args: Dict[str, any]):
        self._actions[action] = args

    def move(self, x: int, y: int):
        if (abs(self._x - x) > self.stats[StatType.SPEED].value() or
                abs(self._y - y) > self.stats[StatType.SPEED].value()):
            raise ValueError("Move is out of bounds")

        if not REGIONS[self._region].is_passable(x, y):
            raise ValueError("Move is blocked")

        raise NotImplementedError

    def step(self):
        if MovableActionType.MOVE in self._actions:
            if "x" in self._actions[MovableActionType.MOVE] and "y" in self._actions[MovableActionType.MOVE]:
                self.move(self._actions[MovableActionType.MOVE]["x"], self._actions[MovableActionType.MOVE]["y"])
            else:
                raise ValueError("Move missing x,y coordinates")

        self._actions = {}
        super().step()
