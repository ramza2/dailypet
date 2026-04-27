from datetime import datetime
from typing import Optional

class DogWalk:
    def __init__(
        self,
        idt_walk: Optional[int] = None,
        idt_pet: Optional[int] = None,
        uid: Optional[str] = None,
        walk_dt: Optional[str] = None,
        walk_distance: Optional[float] = None,
        walk_minute: Optional[int] = None,
    ):
        self.idt_walk = idt_walk
        self.idt_pet = idt_pet
        self.uid = uid
        self.walk_dt = walk_dt
        self.walk_distance = walk_distance
        self.walk_minute = walk_minute

    @classmethod
    def from_dict(cls, data: dict) -> 'DogWalk':
        return cls(
            idt_walk=data.get('idt_walk'),
            idt_pet=data.get('idt_pet'),
            uid=data.get('uid'),
            walk_dt=data.get('walk_dt'),
            walk_distance=data.get('walk_distance'),
            walk_minute=data.get('walk_minute'),
        )

    def to_dict(self) -> dict:
        return {
            'idt_walk': self.idt_walk,
            'idt_pet': self.idt_pet,
            'uid': self.uid,
            'walk_dt': self.walk_dt,
            'walk_distance': self.walk_distance,
            'walk_minute': self.walk_minute,
        } 