from datetime import datetime
from typing import Optional, List, Dict, Any

class DogChat:
    def __init__(
        self,
        id: Optional[int] = None,
        message: Optional[str] = None,
        response: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        dog_id: Optional[int] = None,
        uid: Optional[str] = None,
        message_embedding: Optional[List[float]] = None,
        llm_provider: str = "ollama",
        prompt_template_text: Optional[str] = None
    ):
        self.id = id
        self.message = message
        self.response = response
        self.created_at = created_at
        self.updated_at = updated_at
        self.dog_id = dog_id
        self.uid = uid
        self.message_embedding = message_embedding
        self.llm_provider = llm_provider
        self.prompt_template_text = prompt_template_text
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DogChat":
        """딕셔너리에서 DogChat 객체를 생성합니다."""
        return cls(
            id=data.get("id"),
            message=data.get("message"),
            response=data.get("response"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            dog_id=data.get("dog_id"),
            uid=data.get("uid"),
            message_embedding=data.get("message_embedding"),
            llm_provider=data.get("llm_provider", "ollama"),
            prompt_template_text=data.get("prompt_template_text")
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """DogChat 객체를 딕셔너리로 변환합니다."""
        return {
            "id": self.id,
            "message": self.message,
            "response": self.response,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "dog_id": self.dog_id,
            "uid": self.uid,
            "message_embedding": self.message_embedding,
            "llm_provider": self.llm_provider,
            "prompt_template_text": self.prompt_template_text
        }