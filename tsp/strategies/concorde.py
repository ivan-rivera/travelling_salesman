"""
Concorde solver. This is meant to be the state of the art algorithm

This is meant to serve as a benchmark for other algorithms. If anything
else can come close to Concorde, then it must be pretty good
"""

from logging import getLogger
from typing import List

from concorde.tsp import TSPSolver

from tsp import tools
from tsp.coordinates import Coordinate
from tsp.evaluation import Result

logger = getLogger(__name__)


def find_path(coordinates: List[Coordinate], **kwargs) -> Result:
    logger.info("Finding a path using the Concorde algorithm...")
    xs, ys = [c.x for c in coordinates], [c.y for c in coordinates]
    solver = TSPSolver.from_data(xs, ys, norm="GEOM", name="TSP")
    solution = solver.solve(verbose=False)
    tour = solution.tour.tolist()[1:]
    return Result(tools.create_custom_path(coordinates, tour))
