import logging
from collections import defaultdict
from datetime import date
from typing import Dict, List

from decision_maker.entities.deserted_vehicle_identification import DesertedVehicle, \
    DesertedVehicleIdentificationResults
from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig
from decision_maker.entities.vehicle_identifications import CameraIdentifications, IdentifiedVehicle
from decision_maker.services.vehicles_matching.vehicle_matching_service import BaseVehicleMatchingService


class DesertedVehicleIdentifier:

    def __init__(self, config: DesertedVehicleIdentifierConfig, vehicles_matching_service: BaseVehicleMatchingService):
        self._days_window = config.days_window
        self._min_identification_days = config.min_identification_days
        self._vehicles_matching_service = vehicles_matching_service

    def _is_vehicle_identified_in_list(self, target_vehicle: IdentifiedVehicle,
                                       identified_vehicles: List[IdentifiedVehicle]) -> bool:

        return any([vehicle for vehicle in identified_vehicles if
                    self._vehicles_matching_service.are_same_vehicle(vehicle, target_vehicle)])

    def _is_deserted_vehicle(self, target_vehicle: IdentifiedVehicle,
                             date_to_identified_vehicles: Dict[date, List[IdentifiedVehicle]]):

        matched_dates = [(date) for (date, dates_identified_vehicles) in date_to_identified_vehicles.items() if
                         self._is_vehicle_identified_in_list(target_vehicle, dates_identified_vehicles)]

        return len(matched_dates) > self._min_identification_days

    def identify_deserted_vehicles(self,
                                   camera_identification: CameraIdentifications) -> DesertedVehicleIdentificationResults:

        if camera_identification is None:
            raise ValueError("camera_identification cant be null")

        identified_vehicles = camera_identification.identified_vehicles
        date_to_identified_vehicles = defaultdict(lambda: [])

        for identified_vehicle in identified_vehicles:
            date_to_identified_vehicles[identified_vehicle.date].append(identified_vehicle)

        last_date = sorted(date_to_identified_vehicles.keys())[-1]
        last_date_vehicles = date_to_identified_vehicles[last_date]
        del date_to_identified_vehicles[last_date]

        if len(date_to_identified_vehicles) < self._days_window:
            logging.info(f"not enough days required {self._days_window} have {len(date_to_identified_vehicles)}")
            return DesertedVehicleIdentificationResults(camera_identification.camera_id, None)
        elif len(date_to_identified_vehicles) > self._days_window:
            valid_dates = sorted(date_to_identified_vehicles.keys(), reverse=True)[0: self._days_window]
            date_to_identified_vehicles = {key: value for (key, value) in date_to_identified_vehicles.items() if
                                           key in valid_dates}

        deserted_vehicle = [DesertedVehicle(last_seen=last_date,
                                            vehicle_static_properties=vehicle.vehicle_static_properties())
                            for vehicle in last_date_vehicles if
                            self._is_deserted_vehicle(vehicle, date_to_identified_vehicles)]

        return DesertedVehicleIdentificationResults(
            camera_id=camera_identification.camera_id,
            deserted_vehicles=deserted_vehicle if any(deserted_vehicle) else None)
