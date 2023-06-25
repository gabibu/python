

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Surgery:

    surgery_id: int
    start_time: datetime
    end_time: datetime
