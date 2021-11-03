"""
Monte Carlo Tree Search solution of the TSP

The idea is pretty convoluted. If you really want to understand how it works,
I recommend watching this video: https://www.youtube.com/watch?v=ECpuWvv--GU&t=191s&ab_channel=JO
and also checking out this paper: https://www.sciencedirect.com/science/article/pii/S2185556020300286

Before I get into the description, I'd like to point out that the algorithm consists of the following phases:

* Selection
* Expansion
* Simulation (rollout)
* Backpropagation

Here is the gist of how it works:

We start off with the root (home) node and we _expand_ it by generating all possible 1st moves. That way
We will have an array of possibilities such as node 0 -> node 1, node 0 -> node 2,... node 0 -> node N.
Then for each of those possibilities we run a set of simulations until the very end. Let's suppose we
consider the possibility node 0 -> node 1. From node 1 we want to find the next node, let's suppose
it happens to be node 2, then we keep doing this until we visit all nodes. Note that we do not choose the
next node randomly, instead it is based on a function that balances exploration and exploitation, we use
the following function: v_i + C * sqrt(log(N)/n_i) where v_i is the expected final distance of our chosen
partial path, C is a tunable parameter, N is the number of times the root node has been visited and n_i
is the number of times the root extension has been visited. Note that "root node" in this case means whatever
it is that precedes the path continuation we are checking, whereas "root extension" is the root followed by
the new node that we are trying out (because it is possible to take the same path twice in a simulation). In
order to run these computations we need to keep track of a lookup table with the paths that we've observed
so far. We keep updating this table over the course of our simulations and when we reach the end, it is time
to choose what node we want to append to our root. Let's say our root is node 0 and the best continuation
is node 1 (it's the optimal with minimal expected distance), so we set "node 0 -> node 1" as the new root
and we repeat the whole process all over again. We keep doing this until we visit all nodes. Simple :)
"""

import math
import random
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from typing import List, Dict, DefaultDict, Union, Tuple

from numpy import argmin

from tsp import evaluation
from tsp.coordinates import Coordinate

Lookup = DefaultDict[str, Dict[str, Union[float, int]]]
CoordinatesWithPossibilities = List[Tuple[List[Coordinate], List[Coordinate]]]


_DEFAULT_SIMS = 10
_DEFAULT_EXPLORATION_CRITERION = 10

_ID_SEPARATOR = "-"


def find_path(coordinates: List[Coordinate], **kwargs) -> Dict[str, list]:
    first, rest = coordinates[0], coordinates[1:]
    starting_distance = evaluation.get_total_distance(coordinates + [first])
    lookup = defaultdict(lambda: {"n": 0, "distance": starting_distance})
    return _build_tree([first], rest, lookup, [starting_distance], **kwargs)


def _build_tree(
        root: List[Coordinate],
        candidates: List[Coordinate],
        lookup: Lookup,
        distances: List[float],
        **kwargs
) -> Dict[str, list]:
    expanded_root = _expand(root, candidates)
    evaluated_candidates, new_lookup = _simulate(expanded_root, lookup, **kwargs)
    selection, _ = expanded_root[argmin(evaluated_candidates)]
    new_candidates = [c for c in candidates if c.id != selection[-1].id]
    updated_distances = distances + evaluated_candidates
    return _build_tree(
        selection,
        new_candidates,
        new_lookup,
        updated_distances,
        **kwargs
    ) if new_candidates else {
        "path": selection + [root[0]],
        "history": updated_distances
    }


def _simulate(candidates: CoordinatesWithPossibilities, lookup: Lookup, **kwargs) -> Tuple[List[float], Lookup]:
    new_lookup = lookup.copy()
    for extended_root, possibilities in candidates:
        for _ in range(kwargs.get("sims", _DEFAULT_SIMS)):
            new_lookup = _find_best_leaf(extended_root, possibilities, new_lookup, **kwargs)
    short_lookup = _agg_lookup(new_lookup, len(candidates[0][0]))
    expected_continuation_distance = [
        result["distance"] for root, _ in candidates if (
            root_id := _path_to_id(root),
            result := short_lookup[root_id]
        )]
    return expected_continuation_distance, new_lookup


def _find_best_leaf(root: List[Coordinate], possibilities: List[Coordinate], lookup: Lookup, **kwargs) -> Lookup:
    updated_lookup = lookup.copy()
    updated_root, updated_possibilities = root.copy(), sorted(possibilities, key=lambda _x: random.random())
    while updated_possibilities:
        root_path_id = _path_to_id(updated_root)
        current_lookup = _agg_lookup(updated_lookup, _get_id_length(root_path_id)+1)
        root_lookup = _agg_lookup(updated_lookup, _get_id_length(root_path_id))
        rf = root_lookup[root_path_id]["n"]
        extension_weights = _calculate_weights(updated_root, updated_possibilities, current_lookup, rf, **kwargs)
        updated_root.append(updated_possibilities.pop(int(argmin(extension_weights))))
    chosen_path = updated_root + [root[0]]
    built_path_id = _path_to_id(chosen_path)
    path_distance = evaluation.get_total_distance(chosen_path)
    observed_stats = updated_lookup[built_path_id]
    new_entry = {
        built_path_id: {
            "n": 1 + observed_stats["n"],
            "distance": path_distance,
        }
    }
    updated_lookup.update(new_entry)
    return updated_lookup


def _calculate_weights(
        root: List[Coordinate],
        possibilities: List[Coordinate],
        lookup: Lookup,
        rf: int,
        **kwargs
) -> List[float]:
    return [
        expected_distance - exploration_criterion * exploration_weight
        for p in possibilities if (
            extended_path := _path_to_id(root + [p]),
            values := lookup[extended_path],
            exploration_criterion := kwargs.get("exploration_criterion", _DEFAULT_EXPLORATION_CRITERION),
            expected_distance := values["distance"],
            exploration_weight := math.sqrt(math.log(rf + 1) / (values["n"] + 1))
        )]


def _agg_lookup(lookup: Lookup, length: int) -> Lookup:
    agg_lookup = lookup.copy()
    partial_lookup = [(_get_sub_path_id(path, length), v["n"], v["distance"]) for path, v in agg_lookup.items()]
    grouped = groupby(partial_lookup, key=itemgetter(0))
    new_entries = {k: {
        "n": sum(n for _, n, _ in content),
        "distance": sum(d for _, _, d in content)/len(content)
    } for k, g in grouped if (content := list(g))}
    agg_lookup.update(new_entries)
    return agg_lookup


def _expand(root: List[Coordinate], candidates: List[Coordinate]) -> CoordinatesWithPossibilities:
    return [(root + [c], candidates[:i] + candidates[i+1:]) for i, c in enumerate(candidates)]


def _path_to_id(path: List[Coordinate]) -> str:
    return _ID_SEPARATOR.join(str(i.id) for i in path)


def _get_sub_path_id(path_id: str, length: int):
    return _ID_SEPARATOR.join(path_id.split(_ID_SEPARATOR)[:length])


def _get_id_length(path_id: str) -> int:
    return path_id.count(_ID_SEPARATOR)+1
