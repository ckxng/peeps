from lib.basemap import BaseMapEntity


class Wall(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)

    def __str__(self):
        return "#"
