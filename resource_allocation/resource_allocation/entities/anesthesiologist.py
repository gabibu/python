

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Anesthesiologist:

    anesthesiologists_id: int  = field(compare = True)
    last_allocated_room_id: int  = field(default = None, compare = False)
    last_completed_surgery_time: datetime = field(default = None, compare = False)
