

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Room:

    room_id: int = field(compare = True)
    availabe_time: datetime = field(default = None, compare = False)
