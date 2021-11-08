"""
Simulated annealing solution of the TSP

Reference: https://en.wikipedia.org/wiki/Simulated_annealing

This is how it works:
First, we are going to create a random path and measure its distance.
In each iteration we will randomly switch 2 adjacent destinations, so
if our current order is A->B->C->D->A we can switch B and C places to
get an alternative path A->C->B->D->A. Now we need to measure the
distance covered by both of these paths (old and new). We then replace
our current best path with the new path if (1) the new distance is
shorter or (2) randomly with certain probability. The probability
is based on a comparison between a random uniform value and a function
of the gap between two distances as well as the current temperature
(a parameter). The idea behind this approach is to allow the algorithm
to explore the solution space randomly and eventually settle on the
better solutions.

Lastly note that I've added some magic here that concerns the cooling
schedule and swap count
"""

import math
import random
from typing import List, Dict
from logging import getLogger
from tsp import evaluation, tools
from tsp.coordinates import Coordinate
from tsp.evaluation import Result

logger = getLogger(__name__)

_DEFAULT_TEMPERATURE_SCALE = 10
_DEFAULT_ITERATIONS = 10000
_DEFAULT_COOLING = 0.001
_DEFAULT_SWAP_COUNT_MAX = 3
_DEFAULT_SWAP_COUNT_START_SCALE = 4


def find_path(coordinates: List[Coordinate], **kwargs) -> Result:
    logger.info("Finding a path using the SA algorithm...")
    history = []
    temperature_scale = kwargs.get("temperature_scale", _DEFAULT_TEMPERATURE_SCALE)
    iterations = kwargs.get("iterations", _DEFAULT_ITERATIONS)
    circled_path = coordinates + [coordinates[0]]
    for i in range(iterations):
        alternative_path = circled_path.copy()
        temperature = temperature_scale * (1-math.pow(i/iterations, kwargs.get("cooling", _DEFAULT_COOLING)))
        swap_count = 1 + (1-math.pow(i/iterations, 0.1)) * len(coordinates) // _DEFAULT_SWAP_COUNT_START_SCALE
        random_extra_swaps = random.randint(0, _DEFAULT_SWAP_COUNT_MAX)
        for _ in range(int(swap_count) + random_extra_swaps):
            selected1, selected2 = random.sample([j + 1 for j in range(len(alternative_path) - 3)], 2)
            alternative_path = tools.swap_coordinates(alternative_path, selected1, selected2)
        alternative_length = evaluation.get_total_distance(alternative_path)
        current_length = evaluation.get_total_distance(circled_path)
        annealed_diff = (current_length - alternative_length) / temperature
        metropolis_acceptance = math.exp(annealed_diff) if annealed_diff < 0 else 1
        if alternative_length < current_length or random.random() < metropolis_acceptance:
            circled_path, current_length = alternative_path, alternative_length
        history.append(current_length)
    return Result(circled_path, history)
