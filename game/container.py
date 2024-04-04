from functools import wraps
from typing import Dict

from const.resource import ResourceType


def container_trait(cls):
    @wraps(cls)
    def decorator(*args, **kwargs):
        contents: Dict[ResourceType, int] = {}
        for t in ResourceType:
            contents[t] = 0
        setattr(cls, 'contents', contents)
        return cls

    return decorator
