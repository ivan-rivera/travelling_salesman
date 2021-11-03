"""Supporting functions"""

from time import perf_counter
from functools import wraps
from typing import List

from tsp.coordinates import Coordinate, CoordinateId


def timer(f):
    """Decorator that measures time (seconds) and returns it with the result of the function"""
    @wraps(f)
    def g(*args, **kwargs):
        start = perf_counter()
        result = f(*args, **kwargs)
        time_elapsed = perf_counter() - start
        return {"result": result, "elapsed": time_elapsed}
    return g


def create_custom_path(coordinates: List[Coordinate], order: List[int]) -> List[Coordinate]:
    """Given a set of coordinates, pass your own desired order (excluding the origin) to complete the route"""
    if len(coordinates)-1 != len(order):
        raise ValueError("length of order must be length of coordinates minus 1 (exclude origin)")
    order_with_origin = [0] + order
    indexed_order = sorted(zip(order_with_origin, [i for i in range(len(order_with_origin))]), key=lambda x: x[0])
    coordinate_order = sorted(zip(coordinates, [i[1] for i in indexed_order]), key=lambda x: x[1])
    return [p for (p, _) in coordinate_order] + [coordinates[0]]


def swap_coordinates(coordinates: List[Coordinate], a: CoordinateId, b: CoordinateId) -> List[Coordinate]:
    """Given a set of coordinates, swap coordinate IDs A and B places"""
    a_index, b_index = [index for index, coord in enumerate(coordinates) if coord.id in (a, b)]
    new_coord = coordinates.copy()
    new_coord[a_index], new_coord[b_index] = new_coord[b_index], new_coord[a_index]
    return new_coord

