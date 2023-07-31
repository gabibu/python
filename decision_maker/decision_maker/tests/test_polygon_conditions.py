import unittest
from datetime import date

from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig
from decision_maker.entities.shapes import PolygonCoordinates, Point
from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.shapes.intersection_calculator import IouIntersectionCalculator
from decision_maker.services.vehicles_matching.same_vehicle_conditions.polygon_condition import PolygonCondition


class TestPolygonConditions(unittest.TestCase):

    def _create_polygon_condition(self, config: DesertedVehicleIdentifierConfig,
                                  intersection_calculator=IouIntersectionCalculator()) -> PolygonCondition:
        return PolygonCondition(config=config, intersection_calculator=intersection_calculator)

    def test_no_intersection(self):
        condition = self._create_polygon_condition(DesertedVehicleIdentifierConfig(10, 0.5, 10))

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        self.assertFalse(condition.is_matched(v1, v2))

    def test_contains_intersection(self):
        condition = self._create_polygon_condition(DesertedVehicleIdentifierConfig(10, 0.25, 10))

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 100), Point(100, 100), Point(100, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 50), Point(50, 50), Point(50, 0)]),
                               date.today())

        self.assertTrue(condition.is_matched(v1, v2))

    def test_intersection_below_threshold(self):
        condition = self._create_polygon_condition(DesertedVehicleIdentifierConfig(10, 0.3, 10))

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 100), Point(100, 100), Point(100, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 50), Point(50, 50), Point(50, 0)]),
                               date.today())

        self.assertFalse(condition.is_matched(v1, v2))

    def test_full_intersection_threshold(self):
        condition = self._create_polygon_condition(DesertedVehicleIdentifierConfig(10, 1., 10))

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 100), Point(100, 100), Point(100, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t2", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 100), Point(100, 100), Point(100, 0)]),
                               date.today())

        self.assertTrue(condition.is_matched(v1, v2))
