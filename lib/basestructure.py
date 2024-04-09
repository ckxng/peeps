from typing import Dict, Optional

from lib.basemap import BaseMapEntity
from lib.globals import STRUCTURES


class BaseStructureEntity(BaseMapEntity):
    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def __init__(self, region: str, x: int, y: int, controller: Optional[any] = None):
        super().__init__(region=region, x=x, y=y)
        STRUCTURES[self._id] = self
        self._controller = controller
        if self._controller is not None:
            self._controller.add_structure(self)

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
