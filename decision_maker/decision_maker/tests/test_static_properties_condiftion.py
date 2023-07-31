import unittest
from datetime import date

from decision_maker.entities.shapes import PolygonCoordinates, Point
from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.vehicles_matching.same_vehicle_conditions.static_properties_condition import \
    StaticPropertiesCondition


class TestPolygonConditions(unittest.TestCase):

    def _create_static_properties_condition(self) -> StaticPropertiesCondition:
        return StaticPropertiesCondition()

    def test_diffrent_color(self):
        condition = self._create_static_properties_condition()

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c2",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        self.assertFalse(condition.is_matched(v1, v2))

    def test_diffrent_vehicle_type(self):
        condition = self._create_static_properties_condition()

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t2", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        self.assertFalse(condition.is_matched(v1, v2))

    def test_matched_static_properties(self):
        condition = self._create_static_properties_condition()

        v1 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(0, 0), Point(0, 10), Point(5, 10), Point(5, 0)]),
                               date.today())

        v2 = IdentifiedVehicle("t1", "c1",
                               PolygonCoordinates([Point(100, 0), Point(100, 10), Point(200, 10), Point(200, 0)]),
                               date.today())

        self.assertTrue(condition.is_matched(v1, v2))
