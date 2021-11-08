"""
Greedy strategy for finding the optimal route.
Greedy means that we are always looking for the next closest point.
This approach is expected to be much better than random but far from optimal. It is still a benchmark

Note that this approach can also be called Nearest Neighbours
"""
from logging import getLogger

from typing import List, Dict

from tsp.coordinates import Coordinate, CoordinateId
from tsp.evaluation import calculate_distance, Result

logger = getLogger(__name__)


def find_path(coordinates: List[Coordinate], **kwargs) -> Result:
    logger.info("finding a greedy path...")
    first = coordinates[0]
    candidates = {candidate.id: candidate for candidate in coordinates[1:]}
    greedy_path = _find_greedy_path(first, candidates, [first])
    return Result(greedy_path + [first])


def find_closest_point(position: Coordinate, candidates: Dict[CoordinateId, Coordinate]) -> CoordinateId:
    distances = {
        candidate_id: calculate_distance(position, candidate)
        for candidate_id, candidate in candidates.items()
    }
    return min(distances, key=distances.get)


def _find_greedy_path(
        reference: Coordinate,
        candidates: Dict[CoordinateId, Coordinate],
        path: List[Coordinate]
) -> List[Coordinate]:
    remaining_point = list(candidates.keys())[0]
    next_point_id = find_closest_point(reference, candidates) if len(candidates) > 1 else remaining_point
    next_position = candidates.pop(next_point_id)
    updated_path = path + [next_position]
    return _find_greedy_path(next_position, candidates, updated_path) if candidates else updated_path
