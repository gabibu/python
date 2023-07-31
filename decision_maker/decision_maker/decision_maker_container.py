from dependency_injector import containers, providers

from decision_maker.decision_maker_manager import DecisionMakerManager
from decision_maker.entities.deserted_vehicle_identifier_config import DesertedVehicleIdentifierConfig
from decision_maker.services.dal.camera_identifications_service import StaticCameraIdentificationsService
from decision_maker.services.dal.deserted_vehicles_results_collector import DummyDesertedVehiclesResultsCollector
from decision_maker.services.deserted_identifiers.deserted_vehicle_identifier import DesertedVehicleIdentifier
from decision_maker.services.shapes.intersection_calculator import IouIntersectionCalculator
from decision_maker.services.vehicles_matching.same_vehicle_conditions.polygon_condition import PolygonCondition
from decision_maker.services.vehicles_matching.same_vehicle_conditions.static_properties_condition import \
    StaticPropertiesCondition
from decision_maker.services.vehicles_matching.vehicle_matching_service import RulesVehicleMatchingService


class DecisionMakerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    deserted_vehicle_config = providers.Singleton(DesertedVehicleIdentifierConfig, days_window=config.days_window,
                                                  valid_for_intersection_threshold=config.valid_for_intersection_threshold,
                                                  min_identification_days=config.min_identification_days)

    intersection_calculator = providers.Singleton(IouIntersectionCalculator)

    polygon_condition = providers.Singleton(PolygonCondition,
                                            config=deserted_vehicle_config,
                                            intersection_calculator=intersection_calculator)

    stattic_properties_condition = providers.Singleton(StaticPropertiesCondition)

    conditions = providers.List(stattic_properties_condition, polygon_condition)

    vehicle_matching_service = providers.Singleton(RulesVehicleMatchingService, conditions=conditions)

    deserted_vehicle_identifier = providers.Singleton(DesertedVehicleIdentifier, config=deserted_vehicle_config,
                                                      vehicles_matching_service=vehicle_matching_service)

    deserted_vehicles_results_collector = providers.Singleton(DummyDesertedVehiclesResultsCollector)
    camera_identifications_service = providers.Singleton(StaticCameraIdentificationsService, None)

    decision_maker = providers.Factory(DecisionMakerManager,
                                       camera_identifications_service=camera_identifications_service,
                                       deserted_vehicle_identifier=deserted_vehicle_identifier,
                                       deserted_vehicles_results_collector=deserted_vehicles_results_collector)
