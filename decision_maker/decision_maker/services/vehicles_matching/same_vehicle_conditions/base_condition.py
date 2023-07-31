
from abc import ABC, abstractmethod

from decision_maker.entities.vehicle_identifications import IdentifiedVehicle

class BaseCondition(ABC):

    @abstractmethod
    def is_matched(self, vehicle1: IdentifiedVehicle, vehicle2: IdentifiedVehicle) -> bool:
        pass