from datetime import datetime
from dataclasses import dataclass

@dataclass
class Respiration:
    idt_respiration: int = None
    idt_pet: int = None
    uid: str = None
    idt_measure_respiration: int = None
    respiration: int = None
    respiration_dt: datetime = None

    def __post_init__(self):
        if self.respiration_dt is None:
            self.respiration_dt = datetime.now() 