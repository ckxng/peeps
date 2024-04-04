from ent.bot import Bot


class Peep(Bot):
    def __init__(self, region: str, x: int, y: int):
        super().__init__(region=region, x=x, y=x)
        # todo assign player ownership

    def __str__(self):
        return "@"
