from datetime import datetime, date
from typing import Optional

class Pet:
    def __init__(
        self,
        idt_pet: Optional[int] = None,
        uid: str = "",
        name: str = "",
        thumb_type: str = "N",
        thumb_content: Optional[str] = None,
        gender: str = "",
        neutering_yn: str = "",
        birthday: date = None,
        adoption_date: date = None,
        breed: str = "",
        weight: float = 0.0,
        classification: str = "",
        regist_number: Optional[str] = None,
        deleted: bool = False,
        create_dt: Optional[datetime] = None,
        bcs_type: Optional[str] = None,
        health_status: Optional[str] = None,
        health_issues: Optional[str] = None,
        last_checkup_date: Optional[str] = None
    ):
        self.idt_pet = idt_pet
        self.uid = uid
        self.name = name
        self.thumb_type = thumb_type
        self.thumb_content = thumb_content
        self.gender = gender
        self.neutering_yn = neutering_yn
        self.birthday = birthday
        self.adoption_date = adoption_date
        self.breed = breed
        self.weight = weight
        self.classification = classification
        self.regist_number = regist_number
        self.deleted = deleted
        self.create_dt = create_dt
        self.bcs_type = bcs_type
        self.health_status = health_status
        self.health_issues = health_issues
        self.last_checkup_date = last_checkup_date

    @classmethod
    def from_dict(cls, data: dict) -> 'Pet':
        return cls(
            idt_pet=data.get('idt_pet'),
            uid=data['uid'],
            name=data['name'],
            thumb_type=data.get('thumb_type', 'N'),
            thumb_content=data.get('thumb_content'),
            gender=data['gender'],
            neutering_yn=data['neutering_yn'],
            birthday=data['birthday'],
            adoption_date=data['adoption_date'],
            breed=data['breed'],
            weight=data.get('weight', 0.0),
            classification=data['classification'],
            regist_number=data.get('regist_number'),
            deleted=data.get('deleted', False),
            create_dt=data.get('create_dt'),
            bcs_type=data.get('bcs_type'),
            health_status=data.get('health_status'),
            health_issues=data.get('health_issues'),
            last_checkup_date=data.get('last_checkup_date')
        )

    def to_dict(self) -> dict:
        return {
            'idt_pet': self.idt_pet,
            'uid': self.uid,
            'name': self.name,
            'thumb_type': self.thumb_type,
            'thumb_content': self.thumb_content,
            'gender': self.gender,
            'neutering_yn': self.neutering_yn,
            'birthday': self.birthday,
            'adoption_date': self.adoption_date,
            'breed': self.breed,
            'weight': self.weight,
            'classification': self.classification,
            'regist_number': self.regist_number,
            'deleted': self.deleted,
            'create_dt': self.create_dt,
            'bcs_type': self.bcs_type,
            'health_status': self.health_status,
            'health_issues': self.health_issues,
            'last_checkup_date': self.last_checkup_date
        } 