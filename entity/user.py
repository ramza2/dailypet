from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        uid: str,
        push_key: Optional[str] = None,
        id: str = "",
        phone: str = "",
        thumb_type: str = "N",
        thumb_content: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        deleted: bool = False,
        name_changed_dt: Optional[datetime] = None,
        create_dt: Optional[datetime] = None
    ):
        self.uid = uid
        self.push_key = push_key
        self.id = id
        self.phone = phone
        self.thumb_type = thumb_type
        self.thumb_content = thumb_content
        self.name = name
        self.address = address
        self.deleted = deleted
        self.name_changed_dt = name_changed_dt
        self.create_dt = create_dt

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            uid=data['uid'],
            push_key=data.get('push_key'),
            id=data['id'],
            phone=data['phone'],
            thumb_type=data.get('thumb_type', 'N'),
            thumb_content=data.get('thumb_content'),
            name=data.get('name'),
            address=data.get('address'),
            deleted=data.get('deleted', False),
            name_changed_dt=data.get('name_changed_dt'),
            create_dt=data.get('create_dt')
        )

    def to_dict(self) -> dict:
        return {
            'uid': self.uid,
            'push_key': self.push_key,
            'id': self.id,
            'phone': self.phone,
            'thumb_type': self.thumb_type,
            'thumb_content': self.thumb_content,
            'name': self.name,
            'address': self.address,
            'deleted': self.deleted,
            'name_changed_dt': self.name_changed_dt,
            'create_dt': self.create_dt
        } 