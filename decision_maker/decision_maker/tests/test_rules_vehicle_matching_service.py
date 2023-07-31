import unittest
from datetime import date
from unittest.mock import MagicMock

from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig
from decision_maker.entities.shapes import PolygonCoordinates, Point
from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.shapes.intersection_calculator import IouIntersectionCalculator
from decision_maker.services.vehicles_matching.same_vehicle_conditions.polygon_condition import PolygonCondition
from decision_maker.services.vehicles_matching.same_vehicle_conditions.static_properties_condition import \
    StaticPropertiesCondition
from decision_maker.services.vehicles_matching.vehicle_matching_service import RulesVehicleMatchingService


class TestRulesVehicleMatchingService(unittest.TestCase):

    def test_same_static_polygon_below_threshold(self):
        intersection_threshold = 0.5
        config = DesertedVehicleIdentifierConfig(10, intersection_threshold, 10)
        intersection_calculator = IouIntersectionCalculator()
        intersection_calculator.intersection = MagicMock(return_value=intersection_threshold - 0.1)
        static_properties_condition = StaticPropertiesCondition()
        static_properties_condition.is_matched = MagicMock(return_value=True)
        polygon_condition = PolygonCondition(config, intersection_calculator)

        rules_vehicles_matching_service = RulesVehicleMatchingService([static_properties_condition, polygon_condition])

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        are_same_vehicles = rules_vehicles_matching_service.are_same_vehicle(v1, v2)

        self.assertFalse(are_same_vehicles)

    def test_different_static_properties(self):
        intersection_threshold = 0.5
        config = DesertedVehicleIdentifierConfig(10, intersection_threshold, 10)
        intersection_calculator = IouIntersectionCalculator()
        intersection_calculator.intersection = MagicMock(return_value=intersection_threshold + 0.1)
        static_properties_condition = StaticPropertiesCondition()
        static_properties_condition.is_matched = MagicMock(return_value=False)
        polygon_condition = PolygonCondition(config, intersection_calculator)

        rules_vehicles_matching_service = RulesVehicleMatchingService([static_properties_condition, polygon_condition])

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        are_same_vehicles = rules_vehicles_matching_service.are_same_vehicle(v1, v2)

        self.assertFalse(are_same_vehicles)

    def test_valid_match(self):
        intersection_threshold = 0.5
        config = DesertedVehicleIdentifierConfig(10, intersection_threshold, 10)
        intersection_calculator = IouIntersectionCalculator()
        intersection_calculator.intersection = MagicMock(return_value=intersection_threshold + 0.1)
        static_properties_condition = StaticPropertiesCondition()
        static_properties_condition.is_matched = MagicMock(return_value=True)
        polygon_condition = PolygonCondition(config, intersection_calculator)

        rules_vehicles_matching_service = RulesVehicleMatchingService([static_properties_condition, polygon_condition])

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        are_same_vehicles = rules_vehicles_matching_service.are_same_vehicle(v1, v2)

        self.assertTrue(are_same_vehicles)
