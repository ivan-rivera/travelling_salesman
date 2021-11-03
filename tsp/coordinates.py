"""
Coordinate structures and functions
"""

from typing import List, NewType
from random import random
from dataclasses import dataclass


CoordinateId = NewType("CoordinateId", int)


@dataclass
class Coordinate:
    id: CoordinateId
    x: float
    y: float


def create_coordinates(length: int) -> List[Coordinate]:
    """Generate our problem space given the desired number of coordinates (length)"""
    if length > 100:
        raise ValueError("The length is way too high!")
    return [Coordinate(id=CoordinateId(i), x=random(), y=random()) for i in range(length)]
