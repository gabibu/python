

from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.vehicles_matching.same_vehicle_conditions.base_condition import BaseCondition


class StaticPropertiesCondition(BaseCondition):

    def is_matched(self, vehicle1: IdentifiedVehicle, vehicle2: IdentifiedVehicle) -> bool:
        return vehicle1.vehicle_static_properties() == vehicle2.vehicle_static_properties()