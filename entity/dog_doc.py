from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class DogDoc(BaseModel):
    id: Optional[int] = None
    content: str
    embedding: List[float]
    source: str  # 파일명이나 문서 출처를 저장
    created_at: datetime
    updated_at: Optional[datetime] = None
    loader_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DogDoc':
        """딕셔너리에서 DogDoc 객체를 생성합니다."""
        if hasattr(data, 'items'):
            data = dict(data)
            
        # 임베딩이 문자열인 경우 List[float]로 변환
        embedding = data['embedding']
        if isinstance(embedding, str):
            embedding = [float(x) for x in embedding.strip('[]').split(',')]
            
        return cls(
            id=data['id'],
            content=data['content'],
            embedding=embedding,
            created_at=data['created_at'],
            updated_at=data.get('updated_at'),
            source=data.get('source', ''),
            loader_type=data.get('loader_type')
        )
        
    def to_dict(self) -> dict:
        """DogDoc 객체를 딕셔너리로 변환합니다."""
        return {
            'id': self.id,
            'content': self.content,
            'embedding': self.embedding,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'source': self.source,
            'loader_type': self.loader_type
        } 