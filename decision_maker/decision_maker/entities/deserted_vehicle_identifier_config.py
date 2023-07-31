from dataclasses import dataclass


@dataclass
class DesertedVehicleIdentifierConfig:
    days_window: int
    valid_for_intersection_threshold: float
    min_identification_days: int

    def __post_init__(self):
        if self.days_window < self.min_identification_days:
            raise ValueError(
                f"days_window {self.days_window} is smaller than min_identification_days {self.min_identification_days}")
