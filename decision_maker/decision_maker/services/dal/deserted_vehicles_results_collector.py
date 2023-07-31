import logging
from abc import ABC, abstractmethod

from decision_maker.entities.deserted_vehicle_identification import DesertedVehicleIdentificationResults


class DesertedVehiclesResultsCollector(ABC):

    @abstractmethod
    def collect(self, deserted_vehicle_identification_results: DesertedVehicleIdentificationResults):
        pass


class DummyDesertedVehiclesResultsCollector(DesertedVehiclesResultsCollector):

    def collect(self,
                deserted_vehicle_identification_results: DesertedVehicleIdentificationResults):
        logging.info(f"write_deserted_vehicle_results {deserted_vehicle_identification_results}")
