from lib.basecontroller import BaseControllerEntity
from lib.basestructure import BaseStructureEntity


class Spawn(BaseStructureEntity):
    def __init__(self, region: str, x: int, y: int, controller: BaseControllerEntity = None):
        super().__init__(region=region, x=x, y=x, controller=controller)
        # TODO register spawns with a global lookup so they can accept commands

    def __str__(self):
        return "s"
