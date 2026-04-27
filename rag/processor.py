from typing import List
from pathlib import Path
from .loader import DocumentLoader, DocumentLoaderType
from .splitter import DocumentSplitter
from llm.model import get_model
from entity.dog_doc import DogDoc
import logging
from datetime import datetime
import json
from langchain.schema import Document

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, loader: DocumentLoader):
        self.loader = loader
        self.splitter = DocumentSplitter()
        self.model = get_model()

    def process_document(self, texts: List[str], source: str) -> List[DogDoc]:
        """문서를 처리하고 DogDoc 리스트를 반환합니다."""
        try:
            dog_docs = []
            
            # UnstructuredPDFLoader인 경우 별도의 분할 없이 처리
            if self.loader.loader_type == DocumentLoaderType.UNSTRUCTURED:
                for text in texts:
                    if text.strip():  # 빈 텍스트는 제외
                        embedding = self.model.encode(text)
                        dog_doc = DogDoc(
                            content=text,
                            embedding=embedding.tolist(),
                            source=source,
                            loader_type=self.loader.loader_type.value,
                            created_at=datetime.now()
                        )
                        dog_docs.append(dog_doc)
                return dog_docs
            
            # 텍스트를 Document 객체로 변환
            documents = []
            for text in texts:
                if not isinstance(text, str):
                    text = str(text)
                documents.append(Document(page_content=text))
            
            # 문서 분할
            chunks = self.splitter.split_documents(documents)
        
            # 각 청크에 대해 임베딩 생성 및 DogDoc 객체 생성
            for chunk in chunks:
                content = chunk.page_content
                embedding = self.model.encode(content)
                dog_doc = DogDoc(
                    content=content,
                    embedding=embedding,
                    source=source,
                    loader_type=self.loader.loader_type.value,
                    created_at=datetime.now()
                )
                dog_docs.append(dog_doc)
                
            return dog_docs
            
        except Exception as e:
            logger.error(f"문서 처리 중 오류 발생: {str(e)}")
            raise