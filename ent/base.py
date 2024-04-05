from typing import Dict
from uuid import uuid4

from const.stat import Stat, StatType


class BaseEntity:
    def __init__(self, region, x: int, y: int):
        self._id = str(uuid4())
        self._region = region
        self._x = x
        self._y = y
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
    def _stats_to_dict(stats: Dict[StatType, Stat]) -> Dict[str, Dict[str, any]]:
        s = {}
        for k, v in stats.items():
            s[k.name] = v.to_dict()
        return s

    def to_dict(self):
        return {
            "id": self._id,
            "type": self.__class__.__name__,
            "stats": self._stats_to_dict(self.stats),
            "region": self._region,
            "x": self._x,
            "y": self._y,
        }

    def update_location(self, region: str, x: int, y: int):
        self._region = region
        self._x = x
        self._y = y
