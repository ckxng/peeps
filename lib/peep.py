from lib.basemovable import BaseMovableEntity


class Peep(BaseMovableEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=y)

    def __str__(self):
        return "@"
