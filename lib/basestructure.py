from typing import Dict

from lib.basecontroller import BaseControllerEntity
from lib.basemap import BaseMapEntity


class BaseStructureEntity(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int, controller: BaseControllerEntity = None):
        super().__init__(region=region, x=x, y=y)
        self._controller = controller

    def to_dict(self, show_all: bool = False, show_id: bool = False) -> Dict[str, any]:
        return super().to_dict(show_all=show_all, show_id=True)
