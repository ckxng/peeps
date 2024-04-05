from lib.basemap import BaseMapEntity


# @container_trait
class Tile(BaseMapEntity):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)

    def __str__(self):
        return " "

    @staticmethod
    def is_buildable(self):
        return True
