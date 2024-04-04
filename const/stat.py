from enum import Enum
from typing import Dict


class StatType(Enum):
    HEALTH = "health"
    CAPACITY = "capacity"
    SPEED = "speed"
    STRENGTH = "strength"
    ARMOR = "armor"
    SHIELD = "shield"
    LIFETIME = "lifetime"


class Stat:
    def __init__(self, type: StatType, value: int = 0, min: int = 0, max: int = None, natural_step: int = 0,
                 natural: int = 0, immutable: bool = False):
        self._type = type
        self._value = value
        self._min = min
        self._max = max
        self._natural_step = natural_step
        self._natural = natural
        self._immutable = immutable

    def type(self) -> StatType:
        return self._type

    def value(self, value: int = None) -> int:
        if value is not None and not self._immutable:
            self._value = self._limit(value)
        return self._value

    def increment(self, by: int = 1) -> int:
        return self.value(self._limit(self._value + by))

    def decrement(self, by: int = 1) -> int:
        return self.value(self._limit(self._value - by))

    def min(self, value: int = None) -> int:
        if value is not None:
            self._min = value
        return self._min

    def no_min(self):
        self._min = None

    def max(self, value: int = None) -> int:
        if value is not None:
            self._max = value
        return self._max

    def no_max(self):
        self._max = None

    def _limit(self, value: int) -> int:
        if self._max is not None and value > self._max:
            return self._max
        if self._min is not None and value < self._min:
            return self._min
        return value

    def upgrade(self, by: int = 1) -> int:
        self._max += by
        return self.increment(by)

    def downgrade(self, by: int = 1) -> int:
        self._max = self._limit(self._max - by)
        return self.decrement(by)

    def natural(self, value: int = None) -> int:
        if value is not None:
            self._natural = self._limit(value)
        return self._natural

    def natural_step(self, value: int = None) -> int:
        if value is not None:
            self._natural_step = self._limit(value)
        return self._natural_step

    def immutable(self, value: bool = None) -> int:
        if value is not None:
            self._immutable = value
        return self._immutable

    def step(self):
        if self._value > self._natural:
            return self.decrement(self._natural_step)
        elif self._value < self._natural:
            return self.increment(self._natural_step)
        return self._value

    def to_dict(self) -> Dict[str, any]:
        return {
            "type": self._type.name,
            "value": self._value,
            "max": self._max,
            "min": self._min,
            "natural": self._natural,
            "natural_step": self._natural_step,
            "immutable": self._immutable,
        }
