import random
from base64 import b64encode, b64decode
from json import dumps
from math import floor
from typing import List, Optional, Dict
from uuid import uuid4
from zlib import compress, decompress

from ent.bot import Bot
from ent.item import Item
from ent.wall import Wall
from game.source import Source
from game.spawn import Spawn
from game.tile import Tile

DEFAULT_GRID_X = 30
DEFAULT_GRID_Y = 10
MIN_GRID_SIZE = 10


class Region:
    def __init__(self, width=DEFAULT_GRID_X, height=DEFAULT_GRID_Y, seed: int = None):
        """
        Initializes a randomly generated region of size (width, height)
        :param width:
        :param height:
        :param seed:
        """
        if width < MIN_GRID_SIZE or height < MIN_GRID_SIZE:
            raise ValueError(f"minimum Region width and height is {MIN_GRID_SIZE}")

        if seed is not None:
            random.seed(seed)

        self._id = str(uuid4())
        # TODO register regions with a global lookup so entities can find their regions

        self._width = width
        self._height = height

        # passable base layer, walk on
        self._tile_grid = Region._gen_tile_grid(width, height)

        # passable item layer, step over
        self._item_grid = Region._gen_item_grid(width, height)

        # impassable, interact
        self._bot_grid = Region._gen_item_grid(width, height)

        # impassable, walls
        self._wall_grid = Region._gen_wall_grid(self._id, width, height)

    def id(self) -> str:
        return self._id

    @staticmethod
    def _gen_tile_grid(width=DEFAULT_GRID_X, height=DEFAULT_GRID_Y) -> List[List[Tile]]:
        """
        Generates a grid of tiles with Sources randomly spaced
        :param width: grid width (y)
        :param height: grid height (y)
        :return: a grid indexed as [x][y]
        """
        tile_grid: List[List[Tile]] = [[Tile() for _ in range(height)] for _ in range(width)]

        # place sources at least 2 from the edge
        num_sources = random.randint(1, floor((width * height) / 200) + 1)
        for i in range(num_sources):
            tile_grid[random.randint(2, width - 3)][random.randint(2, height - 3)] = Source()

        # place a single spawn point 3 from the edge
        tile_grid[random.randint(3, width - 4)][random.randint(3, height - 4)] = Spawn()
        return tile_grid

    @staticmethod
    def _gen_item_grid(width=DEFAULT_GRID_X, height=DEFAULT_GRID_Y) -> List[List[Optional[Item]]]:
        """
        Generates an empty grid
        :param width: grid width (y)
        :param height: grid height (y)
        :return: a grid indexed as [x][y]
        """
        return [[None for _ in range(height)] for _ in range(width)]

    @staticmethod
    def _gen_bot_grid(width=DEFAULT_GRID_X, height=DEFAULT_GRID_Y) -> List[List[Optional[Bot]]]:
        """
        Generates an empty grid
        :param width: grid width (y)
        :param height: grid height (y)
        :return: a grid indexed as [x][y]
        """
        return [[None for _ in range(height)] for _ in range(width)]

    @staticmethod
    def _gen_wall_grid(region_id: str, width=DEFAULT_GRID_X, height=DEFAULT_GRID_Y) -> List[List[Optional[Wall]]]:
        """
        Generates a grid containing randomly placed walls
        :param width: grid width (y)
        :param height: grid height (y)
        :return: a grid indexed as [x][y]
        """
        # Initialize the map with all passable spaces (False)
        wall_grid: List[List[Optional[Wall]]] = [[None for _ in range(height)] for _ in range(width)]

        # Generate walls in contiguous chunks
        num_walls = random.randint(3, floor((width * height) / 50) + 3)  # Adjust as needed
        for _ in range(num_walls):
            wall_length: int = random.randint(3, 8)  # Adjust as needed
            start_x: int = random.randint(0, width - 1)
            start_y: int = random.randint(0, height - 1)

            # Generate a horizontal or vertical wall
            if random.choice([True, False]):
                # Horizontal wall
                for i in range(wall_length):
                    wall_grid[(start_x + i) % width][start_y] = Wall(region_id, start_x + i, start_y)
            else:
                # Vertical wall
                for i in range(wall_length):
                    wall_grid[start_x][(start_y + i) % height] = Wall(region_id, start_x, start_y + i)

        return wall_grid

    def is_passable(self, x, y):
        return self._bot_grid[x][y] is None

    def _gen_visible_grid(self) -> List[List[any]]:
        """
        Generate the visible grid which will be exposed to the player.  Earlier
        items in this list mask later ones:
        1. walls
        2. bots
        3. items
        4. tiles

        Bots and walls are both impassable, so there should never be a
        conflict in these layers
        :return: str representation of a region
        """
        visible: List[List[any]] = []

        for x in range(self._width):
            visible.append([])
            for y in range(self._height):
                if self._wall_grid[x][y] is not None:
                    visible[x].append(self._wall_grid[x][y])
                elif self._bot_grid[x][y] is not None:
                    visible[x].append(self._item_grid[x][y])
                elif self._item_grid[x][y] is not None:
                    visible[x].append(self._item_grid[x][y])
                else:
                    visible[x].append(self._tile_grid[x][y])

        return visible

    def __str__(self) -> str:
        """
        Render the region within a frame.  Render grids in this order, with
        earlier grids masking later ones:
        1. walls
        2. bots
        3. items
        4. tiles

        Bots and walls are both impassable, so there should never be a
        conflict in these layers
        :return: str representation of a region
        """
        s = ""

        s += "/" + ("-" * self._width) + "\\\n"

        for y in range(self._height):
            s += "|"
            for x in range(self._width):
                cell: str = str(self._tile_grid[x][y])
                if self._wall_grid[x][y] is not None:
                    cell = str(self._wall_grid[x][y])
                elif self._bot_grid[x][y] is not None:
                    cell = str(self._item_grid[x][y])
                elif self._item_grid[x][y] is not None:
                    cell = str(self._item_grid[x][y])
                s += cell
            s += "|\n"

        s += "\\" + ("-" * self._width) + "/"

        return s

    @staticmethod
    def _grid_to_lol(grid: List[List[any]]) -> List[List[Dict[str, any]]]:
        """
        Traverse a grid and render all cells as dicts inside a list of lists
        :param grid:
        :return: a list of lists indexed as [x][y] => dict representing the cell
        """
        g = []
        for grid_x in grid:
            x = []
            for cell in grid_x:
                if cell is not None:
                    x.append(cell.to_dict())
                else:
                    x.append({"type": "None"})
            g.append(x)
        return g

    def to_dict(self, show_all=False) -> Dict[str, any]:
        if show_all:
            return {
                "type": self.__class__.__name__,
                "width": self._width,
                "height": self._height,
                "tile_grid": self._grid_to_lol(self._tile_grid),
                "wall_grid": self._grid_to_lol(self._wall_grid),
                "bot_grid": self._grid_to_lol(self._bot_grid),
                "item_grid": self._grid_to_lol(self._item_grid),
            }

        return {
            "type": self.__class__.__name__,
            "width": self._width,
            "height": self._height,
            "grid": self._grid_to_lol(self._gen_visible_grid()),
        }

    def to_json(self, show_all=False):
        """
        Output a JSON grid representation
        :return: JSON formatted str
        """
        return dumps(self.to_dict(show_all))

    def to_compressed_json(self, show_all=False):
        """
        Output a compressed grid representation
        :return: base64 encoded strong of zlib compressed utf-8 encoded JSON
        """
        return b64encode(compress(bytes(self.to_json(show_all), 'utf-8'))).decode('utf-8')

    @staticmethod
    def compressed_json_to_str(compressed: str) -> str:
        return decompress(b64decode(compressed.encode('utf-8'))).decode('utf-8')

    def step(self):
        """
        Run step for all grid cells.  Process grids in this order:
        1. bots
        2. items
        3. walls
        4. tiles
        """
        for grid in [self._bot_grid]:
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    if grid[x][y] is not None:
                        # run simulation for things that could have moved
                        grid[x][y].update_location(self._id, x, y)
                        grid[x][y].step()

        for grid in [self._item_grid, self._wall_grid, self._tile_grid]:
            for grid_x in self._tile_grid:
                for cell in grid_x:
                    # run simulation for things that can't move
                    cell.step()
