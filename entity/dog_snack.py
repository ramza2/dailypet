from datetime import datetime
from typing import Optional

class DogSnack:
    def __init__(
        self,
        idt_snack: Optional[int] = None,
        idt_pet: Optional[int] = None,
        uid: Optional[str] = None,
        snack_type: Optional[str] = None,
        amount: Optional[float] = None,
        snack_date: Optional[datetime] = None,
        notes: Optional[str] = None
    ):
        self.idt_snack = idt_snack
        self.idt_pet = idt_pet
        self.uid = uid
        self.snack_type = snack_type
        self.amount = amount
        self.snack_date = snack_date
        self.notes = notes

    @classmethod
    def from_dict(cls, data: dict) -> 'DogSnack':
        return cls(
            idt_snack=data.get('idt_snack'),
            idt_pet=data.get('idt_pet'),
            uid=data.get('uid'),
            snack_type=data.get('snack_type'),
            amount=data.get('amount'),
            snack_date=data.get('snack_date'),
            notes=data.get('notes')
        )

    def to_dict(self) -> dict:
        return {
            'idt_snack': self.idt_snack,
            'idt_pet': self.idt_pet,
            'uid': self.uid,
            'snack_type': self.snack_type,
            'amount': self.amount,
            'snack_date': self.snack_date,
            'notes': self.notes
        } 