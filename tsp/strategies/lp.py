"""
Linear programming solution of the TSP.

The idea is simple: we want to define a N*N matrix (where N is the number of nodes)
which will contain the distances from each point to all other points and another
matrix of equal dimensions that will represent paths taken (0s and 1s). We want to
find the paths such that (1) all nodes are visited only once except for node 0
which is visited twice; and (2) the distance is minimised.
"""

from logging import getLogger
from typing import List

import cvxpy as cvx
import numpy as np

from tsp import tools
from tsp.coordinates import Coordinate
from tsp.evaluation import Result

logger = getLogger(__name__)


def find_path(coordinates: List[Coordinate], **kwargs) -> Result:
    logger.info("finding a path based on linear programming...")
    n = len(coordinates)
    distance_matrix = tools.create_distance_matrix(coordinates)
    tour_mask = cvx.Variable(distance_matrix.shape, boolean=True)
    aux = cvx.Variable(n, integer=True)
    ones = np.ones((n, 1))
    objective = cvx.Minimize(cvx.sum(cvx.multiply(distance_matrix, tour_mask)))
    constraints = [
        tour_mask @ ones == ones,  # this and the below constraint impose symmetry requirements
        tour_mask.T @ ones == ones,
        cvx.diag(tour_mask) == 0,  # cannot move to itself
        aux[1:] >= 2,
        aux[1:] <= n,
        aux[0] == 1,
    ]
    for i in range(1, n):
        for j in range(1, n):
            if i != j:  # cannot pass through the same city twice
                constraints += [aux[i] - aux[j] + 1 <= (n - 1) * (1 - tour_mask[i, j])]
    problem = cvx.Problem(objective, constraints)
    problem.solve(verbose=False)
    solution = np.argwhere(tour_mask.value == 1)
    order = solution[0].tolist()
    for i in range(1, n):
        row = order[-1]
        order.append(solution[row, 1])
    return Result(tools.create_custom_path(coordinates, order[1:-1]))
