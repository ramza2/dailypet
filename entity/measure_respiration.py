from datetime import datetime
from dataclasses import dataclass

@dataclass
class MeasureRespiration:
    idt_measure_respiration: int = None
    idt_pet: int = None
    file_path: str = None
    duration: float = None
    phase: int = None
    create_dt: datetime = None

    def __post_init__(self):
        if self.create_dt is None:
            self.create_dt = datetime.now() 