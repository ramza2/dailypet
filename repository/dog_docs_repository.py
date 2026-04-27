from typing import List, Optional
from entity.dog_doc import DogDoc
from datetime import datetime
import asyncpg
import logging

logger = logging.getLogger(__name__)

class DogDocsRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    def _clean_text_for_db(self, text: str) -> str:
        """데이터베이스 저장을 위해 텍스트를 정제합니다."""
        if not text:
            return ""
        # null 바이트 제거
        text = text.replace('\x00', '')
        # 유효하지 않은 UTF-8 문자 제거
        text = text.encode('utf-8', 'ignore').decode('utf-8')
        return text

    async def create_doc(self, content: str, embedding: List[float], source: str, loader_type: str) -> int:
        try:
            # 텍스트 정제
            content = self._clean_text_for_db(content)
            
            async with self.pool.acquire() as conn:
                # embedding을 문자열로 변환
                embedding_str = '[' + ','.join(map(str, embedding)) + ']'
                
                query = """
                INSERT INTO dog_doc (content, embedding, source, loader_type)
                VALUES ($1, $2, $3, $4)
                RETURNING id
                """
                result = await conn.fetchval(query, content, embedding_str, source, loader_type)
                return result
                
        except Exception as e:
            logger.error(f"문서 생성 중 오류 발생: {str(e)}")
            raise

    async def get_doc(self, doc_id: int) -> Optional[DogDoc]:
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT id, content, embedding, source, loader_type, created_at
                FROM dog_doc
                WHERE id = $1
                """
                row = await conn.fetchrow(query, doc_id)
                if row:
                    return DogDoc(
                        id=row['id'],
                        content=row['content'],
                        embedding=row['embedding'],
                        source=row['source'],
                        loader_type=row['loader_type'],
                        created_at=row['created_at']
                    )
                return None
        except Exception as e:
            logger.error(f"문서 조회 중 오류 발생: {str(e)}")
            raise

    async def get_all_docs(self) -> List[DogDoc]:
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT id, content, embedding, source, loader_type, created_at
                FROM dog_doc
                ORDER BY created_at DESC
                """
                rows = await conn.fetch(query)
                return [
                    DogDoc(
                        id=row['id'],
                        content=row['content'],
                        embedding=row['embedding'],
                        source=row['source'],
                        loader_type=row['loader_type'],
                        created_at=row['created_at']
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"문서 목록 조회 중 오류 발생: {str(e)}")
            raise

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨

    async def search_similar_docs(self, query_embedding: List[float], k: int = 3, similarity_threshold: float = 0.5) -> List[DogDoc]:
        """쿼리 임베딩과 유사한 문서를 검색합니다.
        
        Args:
            query_embedding: 검색할 임베딩 벡터
            k: 반환할 최대 문서 수
            similarity_threshold: 최소 유사도 임계값 (0.0 ~ 1.0)
        """
        try:
            async with self.pool.acquire() as conn:
                # query_embedding을 문자열로 변환
                query_embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
                
                query = """
                    SELECT id, content, embedding, source, created_at, loader_type,
                           1 - (embedding <=> $1) as similarity
                    FROM dog_doc
                    WHERE 1 - (embedding <=> $1) >= $3
                    ORDER BY embedding <=> $1
                    LIMIT $2
                """
                results = await conn.fetch(query, query_embedding_str, k, similarity_threshold)
                return [DogDoc.from_dict(dict(row)) for row in results]
        except Exception as e:
            logger.error(f"유사 문서 검색 중 오류 발생: {str(e)}")
            raise
        
    async def update_doc(self, doc_id: int, content: str, embedding: List[float]) -> Optional[DogDoc]:
        """문서를 업데이트합니다."""
        try:
            async with self.pool.acquire() as conn:
                # embedding을 문자열로 변환
                embedding_str = '[' + ','.join(map(str, embedding)) + ']'
                
                query = """
                UPDATE dog_doc
                SET content = $1, embedding = $2::vector
                WHERE id = $3
                RETURNING *
                """
                result = await conn.fetchrow(query, content, embedding_str, doc_id)
                if result:
                    return DogDoc.from_dict(dict(result))
                return None
        except Exception as e:
            logger.error(f"문서 업데이트 중 오류 발생: {str(e)}")
            raise
        
    async def delete_doc(self, doc_id: int) -> bool:
        """문서를 삭제합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = "DELETE FROM dog_doc WHERE id = $1"
                result = await conn.execute(query, doc_id)
                return result == "DELETE 1"
        except Exception as e:
            logger.error(f"문서 삭제 중 오류 발생: {str(e)}")
            raise
            
    async def get_docs_by_source_and_loader(self, source: str, loader_type: str) -> List[DogDoc]:
        """소스와 로더 타입으로 문서를 검색합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT id, content, embedding, source, loader_type, created_at
                FROM dog_doc
                WHERE source = $1 AND loader_type = $2
                ORDER BY id ASC
                """
                rows = await conn.fetch(query, source, loader_type)
                return [
                    DogDoc(
                        id=row['id'],
                        content=row['content'],
                        embedding=[float(x) for x in row['embedding'].strip('[]').split(',')] if row['embedding'] else [],
                        source=row['source'],
                        loader_type=row['loader_type'],
                        created_at=row['created_at']
                    )
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"문서 검색 중 오류 발생: {str(e)}")
            raise
            
    async def get_distinct_sources(self) -> List[str]:
        """distinct한 source 목록을 조회합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT DISTINCT source
                FROM dog_doc
                ORDER BY source
                """
                rows = await conn.fetch(query)
                return [row['source'] for row in rows]
        except Exception as e:
            logger.error(f"source 목록 조회 중 오류 발생: {str(e)}")
            raise
            
    async def get_distinct_loader_types(self, source: str) -> List[str]:
        """특정 source에 대한 distinct한 loader_type 목록을 조회합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT DISTINCT loader_type
                FROM dog_doc
                WHERE source = $1
                ORDER BY loader_type
                """
                rows = await conn.fetch(query, source)
                return [row['loader_type'] for row in rows]
        except Exception as e:
            logger.error(f"loader_type 목록 조회 중 오류 발생: {str(e)}")
            raise 