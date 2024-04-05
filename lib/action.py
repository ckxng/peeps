from lib.base import BaseEntity
from lib.basecontroller import BaseControllerEntity


class Action:
    def __init__(self, actor: BaseControllerEntity, target: BaseEntity):
        self._actor = actor
        self._target = target
