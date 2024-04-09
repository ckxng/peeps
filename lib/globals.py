from json import dumps
from typing import Dict, Any

# cannot typehint because of circular definitions
CONTROLLERS: Dict[str, any] = {}
REGIONS: Dict[str, any] = {}
MOVABLES: Dict[str, any] = {}
STRUCTURES: Dict[str, any] = {}


def entitydict_to_dict(obj: Dict[str, any], show_all: bool = False) -> dict[str, Any]:
    d = {}
    for key, value in obj.items():
        d[key] = value.to_dict(show_all=show_all)
    return d


def entitydict_to_json(obj: Dict[str, any], show_all: bool = False) -> str:
    return dumps(entitydict_to_dict(obj, show_all=show_all))
