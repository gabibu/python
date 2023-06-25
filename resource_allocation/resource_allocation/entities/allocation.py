
from dataclasses import dataclass, field
from datetime import datetime

from resource_allocation.entities.anesthesiologist import Anesthesiologist
from resource_allocation.entities.room import Room

@dataclass
class Allocation:

    surgery_id: int
    room: Room
    anesthesiologist: Anesthesiologist
    start_time: datetime = None
    end_time: datetime = None

    def __lt__(self, other):
        return self.end_time < other.end_time
