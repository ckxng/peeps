from json import dumps
from typing import Dict
from uuid import uuid4

from lib.basemovable import BaseMovableEntity
from lib.basestructure import BaseStructureEntity
from lib.globals import CONTROLLERS, entitydict_to_dict


class BaseControllerEntity:
    def __init__(self):
        self._id = str(uuid4())
        CONTROLLERS[self._id] = self
        self._structures: Dict[str, BaseStructureEntity] = {}
        self._movable: Dict[str, BaseMovableEntity] = {}

    def __del__(self):
        for k, v in self._structures.items():
            self._structures[k].no_controller()
            del self._structures[k]
        for k, v in self._movable.items():
            self._movable[k].no_controller()
            del self._movable[k]

    def id(self):
        return self._id

    def add_structure(self, structure: BaseStructureEntity):
        structure.controller(self)
        self._structures[structure.id()] = structure

    def remove_structure(self, structure: BaseStructureEntity):
        structure.no_controller()
        del self._structures[structure.id()]

    def add_movable(self, movable: BaseMovableEntity):
        movable.controller(self)
        self._movable[movable.id()] = movable

    def remove_movable(self, movable: BaseMovableEntity):
        movable.no_controller()
        del self._movable[movable.id()]

    def to_dict(self, show_all: bool = False) -> Dict[str, any]:
        if show_all:
            return {
                "type": self.__class__.__name__,
                "id": self._id,
                "structures": entitydict_to_dict(self._structures, show_all=show_all),
                "movable": entitydict_to_dict(self._movable, show_all=show_all),
            }
        return {
            "type": self.__class__.__name__,
            "id": self._id,
        }

    def to_json(self, show_all=False) -> str:
        """
        Output a JSON grid representation
        :return: JSON formatted str
        """
        return dumps(self.to_dict(show_all=show_all))
