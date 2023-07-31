from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Generator, Optional
import numpy as np

from decision_maker.entities.shapes import PolygonCoordinates, Point
from decision_maker.entities.vehicle_identifications import CameraIdentifications, IdentifiedVehicle


class BaseCameraIdentificationsService(ABC):

    @abstractmethod
    def get_camera_identifications(self, timeout_seconds: int = 60) -> CameraIdentifications:
        pass


class StaticCameraIdentificationsService(BaseCameraIdentificationsService):

    def __init__(self, cameras_identifications: Optional[List[CameraIdentifications]] = None):
        self._index = 0
        self._cameras_identifications = [
            CameraIdentifications("c1", 1, [IdentifiedVehicle("dsa", "ds", PolygonCoordinates([Point(0, 0), Point(0, 3),
                                                                                               Point(10, 3),
                                                                                               Point(10, 0)]),
                                                              date.today() - timedelta(days=i)) for i in
                                            range(20)])] if cameras_identifications is None else cameras_identifications

    def get_camera_identifications(self, timeout_seconds: int = 60) -> CameraIdentifications:

        index = np.random.randint(0, high=len(self._cameras_identifications), size=1, dtype=int)[0]
        return self._cameras_identifications[index]




