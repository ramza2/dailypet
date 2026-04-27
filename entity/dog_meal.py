from datetime import datetime
from typing import Optional

class DogMeal:
    def __init__(
        self,
        idt_feed: Optional[int] = None,
        idt_pet: Optional[int] = None,
        uid: Optional[str] = None,
        feed_type: Optional[str] = None,
        amount: Optional[float] = None,
        feed_dt: Optional[datetime] = None,
        notes: Optional[str] = None
    ):
        self.idt_feed = idt_feed
        self.idt_pet = idt_pet
        self.uid = uid
        self.feed_type = feed_type
        self.amount = amount
        self.feed_dt = feed_dt
        self.notes = notes

    @classmethod
    def from_dict(cls, data: dict) -> 'DogMeal':
        return cls(
            idt_feed=data.get('idt_feed'),
            idt_pet=data.get('idt_pet'),
            uid=data.get('uid'),
            feed_type=data.get('feed_type'),
            amount=data.get('amount'),
            feed_dt=data.get('feed_dt'),
            notes=data.get('notes')
        )

    def to_dict(self) -> dict:
        return {
            'idt_feed': self.idt_feed,
            'idt_pet': self.idt_pet,
            'uid': self.uid,
            'feed_type': self.feed_type,
            'amount': self.amount,
            'feed_dt': self.feed_dt,
            'notes': self.notes
        } 