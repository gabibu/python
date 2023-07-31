from dataclasses import dataclass
from datetime import date
from typing import Optional, List

from decision_maker.entities.vehicle_identifications import IdentifiedVehicleStaticProperties


@dataclass
class DesertedVehicle:
    last_seen: date
    vehicle_static_properties: IdentifiedVehicleStaticProperties


@dataclass
class DesertedVehicleIdentificationResults:
    camera_id: str
    deserted_vehicles: Optional[List[DesertedVehicle]]
