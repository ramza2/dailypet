from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

class DocumentSplitter:
    def __init__(self, chunk_size: int = 4000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """문서를 청크로 분할합니다."""
        try:
            return self.splitter.split_documents(documents)
            
        except Exception as e:
            logger.error(f"문서 분할 중 오류 발생: {str(e)}")
            raise 