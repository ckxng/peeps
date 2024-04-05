from lib.basecontroller import BaseControllerEntity
from lib.basemap import BaseMapEntity


class BaseStructureEntity(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int, controller: BaseControllerEntity = None):
        super().__init__(region=region, x=x, y=x)
        self._controller = controller
