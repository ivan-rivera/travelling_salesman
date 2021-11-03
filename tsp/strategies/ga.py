"""Genetic algorithm solution of the TSP"""

from typing import List, Dict

from tsp.coordinates import Coordinate


def find_path(coordinates: List[Coordinate], **kwargs) -> Dict[str, list]:
    raise NotImplementedError
