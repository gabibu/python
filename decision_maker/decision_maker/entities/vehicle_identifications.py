from dataclasses import dataclass
from datetime import date
from typing import List

from decision_maker.entities.shapes import PolygonCoordinates


@dataclass
class IdentifiedVehicleStaticProperties:
    vehicle_type: str
    vehicle_color: str


@dataclass
class IdentifiedVehicle:
    vehicle_type: str
    vehicle_color: str
    shape: PolygonCoordinates
    date: date

    def vehicle_static_properties(self) -> IdentifiedVehicleStaticProperties:
        return IdentifiedVehicleStaticProperties(vehicle_type=self.vehicle_type,
                                                 vehicle_color=self.vehicle_color)


@dataclass
class CameraIdentifications:
    camera_id: str
    customer_id: int
    identified_vehicles: List[IdentifiedVehicle]
