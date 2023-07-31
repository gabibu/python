from decision_maker.entities.vehicle_identifications import IdentifiedVehicle
from decision_maker.services.shapes.intersection_calculator import IntersectionCalculator
from decision_maker.services.vehicles_matching.same_vehicle_conditions.base_condition import BaseCondition
from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig

class PolygonCondition(BaseCondition):

    def __init__(self, config: DesertedVehicleIdentifierConfig, intersection_calculator: IntersectionCalculator):
        self._intersection_calculator = intersection_calculator
        self._valid_for_intersection_threshold = config.valid_for_intersection_threshold

    def is_matched(self, vehicle1: IdentifiedVehicle, vehicle2: IdentifiedVehicle) -> bool:
        return self._intersection_calculator.intersection(vehicle1.shape,
                                                          vehicle2.shape) >= self._valid_for_intersection_threshold