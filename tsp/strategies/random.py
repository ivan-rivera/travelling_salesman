"""
Random path algorithm for benchmarking.

This strategy simple shuffles the candidate points to select the path
"""

from logging import getLogger
from random import random
from typing import List, Dict

from tsp.coordinates import Coordinate

logger = getLogger(__name__)


def find_path(coordinates: List[Coordinate], **kwargs) -> Dict[str, list]:
    logger.info("finding random path...")
    first, rest = coordinates[0], coordinates[1:]
    shuffled_rest = sorted(rest, key=lambda _x: random())
    return {
        "path": [first] + shuffled_rest + [first],
        "history": [],
    }
