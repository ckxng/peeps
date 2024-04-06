from lib.basecontroller import BaseControllerEntity
from lib.basestructure import BaseStructureEntity


class Box(BaseStructureEntity):
    def __init__(self, region: str, x: int, y: int, controller: BaseControllerEntity = None):
        super().__init__(region=region, x=x, y=y, controller=controller)

    def __str__(self):
        return "U"
