from abc import ABC, abstractmethod

from decision_maker.entities.shapes import PolygonCoordinates
from decision_maker.utils.geometry_utils import calculate_iou


class IntersectionCalculator(ABC):

    @abstractmethod
    def intersection(self, polygon1: PolygonCoordinates, polygon2: PolygonCoordinates) -> float:
        pass


class IouIntersectionCalculator(IntersectionCalculator):

    def intersection(self, polygon1: PolygonCoordinates, polygon2: PolygonCoordinates) -> float:
        return calculate_iou(polygon1, polygon2)