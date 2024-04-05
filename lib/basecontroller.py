from uuid import uuid4


class BaseControllerEntity:
    def __init__(self):
        self._id = str(uuid4())

    def id(self):
        return self._id
