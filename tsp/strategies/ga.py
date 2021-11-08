"""Genetic algorithm solution of the TSP"""

from typing import List, Dict

from tsp.coordinates import Coordinate
from tsp.evaluation import Result


def find_path(coordinates: List[Coordinate], **kwargs) -> Result:
    raise NotImplementedError
