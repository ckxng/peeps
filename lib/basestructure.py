from enum import Enum
from typing import Dict, Optional

from lib.basemap import BaseMapEntity
from lib.globals import STRUCTURES, REGIONS


class StructureActionType(Enum):
    BUILD = "build"


class BaseStructureEntity(BaseMapEntity):
    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def __init__(self, region: str, x: int, y: int, controller: Optional[any] = None):
        super().__init__(region=region, x=x, y=y)
        STRUCTURES[self._id] = self
        self._controller = controller
        if self._controller is not None:
            self._controller.add_structure(self)
        self._actions: Dict[StructureActionType, Dict[str, any]] = {}

    def __del__(self):
        del STRUCTURES[self._id]
        if self._controller is not None:
            self._controller.remove_structure(self)

    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def controller(self, controller: Optional[any] = None):
        if controller is not None:
            self._controller = controller
        return self._controller

    def no_controller(self):
        self._controller = None

    def to_dict(self, show_all: bool = False, show_id: bool = False) -> Dict[str, any]:
        return super().to_dict(show_all=show_all, show_id=True)

    def add_action(self, action: StructureActionType, args: Dict[str, any]):
        self._actions[action] = args

    def build(self, x: int, y: int):
        if not REGIONS[self._region].is_passable(x, y):
            raise ValueError("Build is blocked")

        raise NotImplementedError

    def step(self):
        if StructureActionType.BUILD in self._actions:
            if "x" in self._actions[StructureActionType.BUILD] and "y" in self._actions[StructureActionType.BUILD]:
                self.build(self._actions[StructureActionType.BUILD]["x"], self._actions[StructureActionType.BUILD]["y"])
            else:
                raise ValueError("Move missing x,y coordinates")

        self._actions = {}
        super().step()
