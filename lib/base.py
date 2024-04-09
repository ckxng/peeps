from json import dumps
from typing import Dict, Optional
from uuid import uuid4

from lib.stat import Stat, StatType


class BaseEntity:
    # controller typehint lib.basecontroller.BaseControllerEntity is circular
    def __init__(self, region, x: int, y: int, controller: Optional[any] = None):
        self._id = str(uuid4())
        self._region = region
        self._x = x
        self._y = y
        self._mind = controller
        self.stats: Dict[StatType, Stat] = {
            StatType.HEALTH: Stat(type=StatType.HEALTH, value=1, max=1),
            StatType.CAPACITY: Stat(type=StatType.CAPACITY, value=0, max=0),
            StatType.SPEED: Stat(type=StatType.SPEED, value=0, max=0),
            StatType.STRENGTH: Stat(type=StatType.STRENGTH, value=0, max=0),
            StatType.ARMOR: Stat(type=StatType.ARMOR, value=0, max=0),
            StatType.SHIELD: Stat(type=StatType.SHIELD, value=0, max=0),
            StatType.LIFETIME: Stat(type=StatType.LIFETIME, value=100, max=100, natural_step=1),
        }
        # TODO register all entities with a global lookup so they can be command targets
        # TODO how does an entity know what its region and grid position is?

    def id(self) -> str:
        return self._id

    def step(self):
        for k in self.stats.keys():
            self.stats[k].step()

    @staticmethod
    def _stats_to_dict(stats: Dict[StatType, Stat], show_all: bool = False) -> Dict[str, Dict[str, any]]:
        s = {}
        for k, v in stats.items():
            if not v.immutable() or show_all:
                s[k.name] = v.to_dict()
        return s

    def to_dict(self, show_all: bool = False, show_id: bool = False) -> Dict[str, any]:
        ret = {
            "type": self.__class__.__name__,
        }
        if show_all or show_id:
            ret['id'] = self._id,
        stats = self._stats_to_dict(self.stats, show_all=show_all)
        if stats:
            ret['stats'] = stats
        if show_all:
            ret['region'] = self._region
            ret['x'] = self._x
            ret['y'] = self._y
        return ret

    def to_json(self, show_all=False) -> str:
        """
        Output a JSON grid representation
        :return: JSON formatted str
        """
        return dumps(self.to_dict(show_all=show_all))

    def update_location(self, region: str, x: int, y: int):
        self._region = region
        self._x = x
        self._y = y
