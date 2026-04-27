from datetime import datetime
from dataclasses import dataclass

@dataclass
class MeasurePulse:
    idt_measure_pulse: int = None
    idt_pet: int = None
    file_path: str = None
    heart_rate: int = None
    ar_per: float = None
    keti_heart_rate: int = None
    keti_ar_per: float = None
    avg_s1_amp: int = None
    max_s1_amp: int = None
    min_s1_amp: int = None
    avg_s1_period: int = None
    max_s1_period: int = None
    min_s1_period: int = None
    s1_count: int = None
    avg_s2_amp: int = None
    max_s2_amp: int = None
    min_s2_amp: int = None
    avg_s2_period: int = None
    max_s2_period: int = None
    min_s2_period: int = None
    s2_count: int = None
    measure_time: int = None
    correct_rate: float = None
    valid_yn: str = None
    raw_temp: str = None
    create_dt: datetime = None

    def __post_init__(self):
        if self.create_dt is None:
            self.create_dt = datetime.now() 