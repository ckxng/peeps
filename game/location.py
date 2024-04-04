class Location:
    def __init__(self):
        pass

    def __str__(self):
        return " "

    def step(self):
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
        }


