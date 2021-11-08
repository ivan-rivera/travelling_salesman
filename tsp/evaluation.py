"""
Evaluation utilities
"""

import math
from dataclasses import dataclass, field
from typing import List, Any, Optional

import matplotlib.pyplot as plt

from tsp.coordinates import Coordinate


@dataclass
class Result:
    path: List[Coordinate]
    history: List[float] = field(default_factory=lambda: [])


def calculate_distance(a: Coordinate, b: Coordinate) -> float:
    """Calculate distance between points A and B"""
    return math.hypot(b.x - a.x, b.y - a.y)


def get_total_distance(paths: List[Coordinate]) -> float:
    """Given a path, find the total distance that it covers"""
    return sum(calculate_distance(paths[p], paths[p+1]) for p in range(len(paths)-1))


def plot_destinations(coordinates: List[Coordinate], title: Optional[str], plot_axes: Optional[Any] = None) -> None:
    """Visualise path taken through the coordinates"""
    xs = [coord.x for coord in coordinates]
    ys = [coord.y for coord in coordinates]
    ids = [coord.id for coord in coordinates]
    plt.figure(figsize=(8, 7))
    ax = plot_axes if plot_axes else plt.axes()
    colours = ["orange"] + ["yellow" for _ in range(len(xs) - 2)]
    for x, y, colour, id_mark in zip(xs, ys, colours, ids):
        ax.scatter(x, y, c=colour, s=100)
        ax.text(x, y, id_mark, c="purple")
    ax.plot(xs, ys, linestyle="dashed")
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.set_title(title)
