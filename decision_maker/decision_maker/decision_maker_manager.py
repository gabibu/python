import logging

from decision_maker.services.dal.camera_identifications_service import BaseCameraIdentificationsService
from decision_maker.services.dal.deserted_vehicles_results_collector import DesertedVehiclesResultsCollector
from decision_maker.services.deserted_identifiers.deserted_vehicle_identifier import DesertedVehicleIdentifier


class DecisionMakerManager:

    def __init__(self, camera_identifications_service: BaseCameraIdentificationsService,
                 deserted_vehicle_identifier: DesertedVehicleIdentifier,
                 deserted_vehicles_results_collector: DesertedVehiclesResultsCollector):
        self._camera_identifications_service = camera_identifications_service
        self._deserted_vehicle_identifier = deserted_vehicle_identifier
        self._deserted_vehicles_results_collector = deserted_vehicles_results_collector

    def run(self):

        while True:

            camera_identification = self._camera_identifications_service.get_camera_identifications()

            deserted_vehicles_identification_result = self._deserted_vehicle_identifier.identify_deserted_vehicles(
                camera_identification)
            logging.info(f"deserted_vehicles_identification_result {deserted_vehicles_identification_result}")
            self._deserted_vehicles_results_collector.collect(deserted_vehicles_identification_result)
