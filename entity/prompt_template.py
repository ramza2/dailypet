from datetime import datetime
from typing import Optional

class PromptTemplate:
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        content: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.content = content
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at
        
    @staticmethod
    def from_dict(data: dict) -> 'PromptTemplate':
        return PromptTemplate(
            id=data.get('id'),
            name=data.get('name', ''),
            content=data.get('content', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        ) 