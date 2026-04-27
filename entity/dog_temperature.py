from datetime import datetime
from typing import Optional

class DogTemperature:
    def __init__(
        self,
        idt_body_heat: Optional[int] = None,
        idt_pet: int = 0,
        uid: str = "",
        idt_measure_pulse: int = 0,
        temp: float = 0.0,
        temp_a : float = 0.0,
        temp_h: float = 0.0,    
        temp_dt: Optional[datetime] = None
    ):
        self.idt_body_heat = idt_body_heat
        self.idt_pet = idt_pet
        self.uid = uid
        self.idt_measure_pulse = idt_measure_pulse
        self.temp = temp
        self.temp_a = temp_a
        self.temp_h = temp_h
        self.temp_dt = temp_dt

    @classmethod
    def from_dict(cls, data: dict) -> 'DogTemperature':
        return cls(
            idt_body_heat=data.get('idt_body_heat'),
            idt_pet=data.get('idt_pet'),
            uid=data.get('uid'),
            idt_measure_pulse=data.get('idt_measure_pulse'),
            temp=data.get('temp', 0.0),
            temp_a=data.get('temp_a', 0.0),
            temp_h=data.get('temp_h', 0.0),
            temp_dt=data.get('temp_dt')
        )

    def to_dict(self) -> dict:
        return {
            'idt_body_heat': self.idt_body_heat,
            'idt_pet': self.idt_pet,
            'uid': self.uid,
            'idt_measure_pulse': self.idt_measure_pulse,
            'temp': self.temp,
            'temp_a': self.temp_a,
            'temp_h': self.temp_h,
            'temp_dt': self.temp_dt
        } 