from dataclasses import dataclass
from datetime import datetime

@dataclass
class EisMeasurement:
    cell_id: int
    creation_time: datetime
    frequency: float
    real_impedance: float
    imag_impedance: float
    voltage: float