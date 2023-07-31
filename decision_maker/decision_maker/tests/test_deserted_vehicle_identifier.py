import unittest
from datetime import date, timedelta, datetime
from unittest.mock import MagicMock, Mock

from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig
from decision_maker.entities.shapes import PolygonCoordinates
from decision_maker.entities.vehicle_identifications import CameraIdentifications, IdentifiedVehicle
from decision_maker.entities.vehicle_identifications import IdentifiedVehicleStaticProperties
from decision_maker.services.deserted_identifiers.deserted_vehicle_identifier import DesertedVehicleIdentifier
from decision_maker.services.vehicles_matching.vehicle_matching_service import RulesVehicleMatchingService


class TestDesertedVehicleIdentifier(unittest.TestCase):

    def test_not_enough_days(self):

        days_window = 10

        config = DesertedVehicleIdentifierConfig(days_window, 0.01, 2)

        rules_vehicle_matching_service = Mock(spec=RulesVehicleMatchingService)

        rules_vehicle_matching_service.are_same_vehicle = MagicMock(return_value=True)
        deserted_vehicles_identifier = DesertedVehicleIdentifier(config, rules_vehicle_matching_service)

        polygon = Mock(spec=PolygonCoordinates)

        camera_identifications = CameraIdentifications("c1", 1, [IdentifiedVehicle("dsa", "ds", polygon,
                                                                                   date.today() - timedelta(days=i)) for
                                                                 i in
                                                                 range(days_window)])

        results = deserted_vehicles_identifier.identify_deserted_vehicles(camera_identifications)

        self.assertIsNone(results.deserted_vehicles)

    def test_not_enough_matched_days(self):
        days_window = 10

        config = DesertedVehicleIdentifierConfig(days_window, 0.01, 6)

        rules_vehicle_matching_service = Mock(spec=RulesVehicleMatchingService)

        rules_vehicle_matching_service.are_same_vehicle = MagicMock(return_value=True)
        deserted_vehicles_identifier = DesertedVehicleIdentifier(config, rules_vehicle_matching_service)

        polygon = Mock(spec=PolygonCoordinates)

        vehicles = [
            IdentifiedVehicle("type1" if i % 2 == 0 else "type2", "color1", polygon, date.today() - timedelta(days=i))
            for
            i in range(days_window)]

        camera_identifications = CameraIdentifications("c1", 1, vehicles)

        results = deserted_vehicles_identifier.identify_deserted_vehicles(camera_identifications)

        self.assertIsNone(results.deserted_vehicles)

    def test_valid_match(self):

        days_window = 10
        start_date = datetime.strptime('07-19-2023', '%m-%d-%Y').date()

        config = DesertedVehicleIdentifierConfig(days_window, 0.01, 5)

        rules_vehicle_matching_service = Mock(spec=RulesVehicleMatchingService)

        rules_vehicle_matching_service.are_same_vehicle = MagicMock(return_value=True)
        deserted_vehicles_identifier = DesertedVehicleIdentifier(config, rules_vehicle_matching_service)

        polygon = Mock(spec=PolygonCoordinates)

        vehicles = [
            IdentifiedVehicle("type1" if i % 2 == 0 else "type2", "color1", polygon, start_date - timedelta(days=i))
            for
            i in range(days_window + 1)]

        camera_identifications = CameraIdentifications("c1", 1, vehicles)

        results = deserted_vehicles_identifier.identify_deserted_vehicles(camera_identifications)

        self.assertIsNotNone(results.deserted_vehicles)
        self.assertEqual(len(results.deserted_vehicles), 1)

        deserted_vehicle = results.deserted_vehicles[0]

        self.assertEqual(deserted_vehicle.last_seen, start_date)
        self.assertEqual(deserted_vehicle.vehicle_static_properties,
                         IdentifiedVehicleStaticProperties(vehicle_type="type1",
                                                           vehicle_color="color1"))

    def test_multiple_vehicles(self):

        expected_static_properties = [IdentifiedVehicleStaticProperties(vehicle_type="type1",
                                                                        vehicle_color="color1"),
                                      IdentifiedVehicleStaticProperties(vehicle_type="type2",
                                                                        vehicle_color="color2")]

        days_window = 10
        start_date = datetime.strptime('07-19-2023', '%m-%d-%Y').date()

        config = DesertedVehicleIdentifierConfig(days_window, 0.01, 5)

        rules_vehicle_matching_service = Mock(spec=RulesVehicleMatchingService)

        rules_vehicle_matching_service.are_same_vehicle = MagicMock(return_value=True)
        deserted_vehicles_identifier = DesertedVehicleIdentifier(config, rules_vehicle_matching_service)

        polygon = Mock(spec=PolygonCoordinates)
        vehicles = []
        for i in range(days_window + 1):
            current_date = start_date - timedelta(days=i)

            date_vehicles = [
                IdentifiedVehicle("type1", "color1", polygon, current_date),
                IdentifiedVehicle("type2", "color2", polygon, current_date),
            ]

            vehicles.extend(date_vehicles)

        camera_identifications = CameraIdentifications("c1", 1, vehicles)

        results = deserted_vehicles_identifier.identify_deserted_vehicles(camera_identifications)

        self.assertIsNotNone(results.deserted_vehicles)
        self.assertEqual(len(results.deserted_vehicles), 2)

        for i in range(2):
            deserted_vehicle = results.deserted_vehicles[i]
            self.assertEqual(deserted_vehicle.last_seen, start_date)
        self.assertEqual(deserted_vehicle.vehicle_static_properties,
                         expected_static_properties[i])
