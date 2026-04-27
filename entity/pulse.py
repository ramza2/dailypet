from datetime import datetime
from dataclasses import dataclass

@dataclass
class Pulse:
    idt_pulse: int = None
    idt_pet: int = None
    uid: str = None
    idt_measure_pulse: int = None
    pulse: int = None
    pulse_dt: datetime = None

    def __post_init__(self):
        if self.pulse_dt is None:
            self.pulse_dt = datetime.now() 