from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: int
    y: int


@dataclass
class PolygonCoordinates:
    points: List[Point]
