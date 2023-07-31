from abc import ABC, abstractmethod
from typing import List

from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.vehicles_matching.same_vehicle_conditions.base_condition import BaseCondition


class BaseVehicleMatchingService(ABC):

    @abstractmethod
    def are_same_vehicle(self, vehicle1: IdentifiedVehicle, vehicle2: IdentifiedVehicle) -> bool:
        pass


class RulesVehicleMatchingService:

    def __init__(self, conditions: List[BaseCondition]):

        if conditions is None or len(conditions) == 0:
            raise ValueError("conditions cant be null or empty")

        self._conditions = conditions

    def are_same_vehicle(self, vehicle1: IdentifiedVehicle, vehicle2: IdentifiedVehicle) -> bool:

        for condition in self._conditions:
            if not condition.is_matched(vehicle1, vehicle2):
                return False

        return True
