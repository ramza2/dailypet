import asyncpg
from typing import List, Optional, Dict, Any
import logging
from entity.dog_chat import DogChat
from datetime import datetime

logger = logging.getLogger(__name__)

class DogChatsRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_chat(self, chat: DogChat) -> DogChat:
        async with self.pool.acquire() as conn:
            # message_embedding을 PostgreSQL vector 타입으로 변환
            vector_str = '[' + ','.join(map(str, chat.message_embedding)) + ']'
            
            row = await conn.fetchrow(
                """
                INSERT INTO dog_chat (
                    message, response, created_at, updated_at, dog_id, uid,
                    message_embedding, llm_provider, prompt_template_text
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7::vector, $8, $9)
                RETURNING *
                """,
                chat.message,
                chat.response,
                chat.created_at,
                chat.updated_at,
                chat.dog_id,
                chat.uid,
                vector_str,
                chat.llm_provider,
                chat.prompt_template_text
            )
            return DogChat.from_dict(row)

    async def get_recent_chats(self, dog_id: int, limit: int = 10, llm_provider: Optional[str] = None) -> List[DogChat]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM dog_chat 
                WHERE dog_id = $1
            """
            params = [dog_id]
            
            if llm_provider:
                query += " AND llm_provider = $" + str(len(params) + 1)
                params.append(llm_provider)
                
            query += " ORDER BY created_at DESC LIMIT $" + str(len(params) + 1)
            params.append(limit)
            
            rows = await conn.fetch(query, *params)
            return [DogChat.from_dict(row) for row in rows]

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 

    async def get_chats_by_pet_and_provider(self, dog_id: int, llm_provider: str, limit: int = 10, offset: int = 0) -> List[DogChat]:
        """특정 반려견의 특정 LLM 제공자에 대한 채팅 이력을 조회합니다. (기존 OFFSET 방식)"""
        try:
            async with self.pool.acquire() as conn:
                query = """
                    SELECT * FROM dog_chat 
                    WHERE dog_id = $1 AND llm_provider = $2
                """
                params = [dog_id, llm_provider]
                
                query += " ORDER BY created_at DESC LIMIT $" + str(len(params) + 1)
                params.append(limit)
                
                query += " OFFSET $" + str(len(params) + 1)
                params.append(offset)
                
                rows = await conn.fetch(query, *params)
                return [DogChat.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting chats: {e}")
            return []

    async def get_chats_by_pet_and_provider_cursor(
        self, 
        dog_id: int, 
        llm_provider: str, 
        limit: int = 10, 
        cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        커서 기반 페이지네이션으로 채팅 이력을 조회합니다.
        
        Args:
            dog_id: 반려견 ID
            llm_provider: LLM 제공자
            limit: 조회할 항목 수
            cursor: 마지막으로 조회한 항목의 created_at (ISO 형식 문자열)
            
        Returns:
            {
                'chats': List[DogChat],
                'next_cursor': Optional[str],
                'has_more': bool
            }
        """
        try:
            async with self.pool.acquire() as conn:
                # 기본 쿼리 구성
                query = """
                    SELECT * FROM dog_chat 
                    WHERE dog_id = $1 AND llm_provider = $2
                """
                params = [dog_id, llm_provider]
                
                # 커서가 있는 경우 조건 추가
                if cursor:
                    try:
                        cursor_datetime = datetime.fromisoformat(cursor.replace('Z', '+00:00'))
                        query += " AND created_at < $" + str(len(params) + 1)
                        params.append(cursor_datetime)
                    except ValueError as e:
                        logger.error(f"Invalid cursor format: {cursor}, error: {e}")
                        return {'chats': [], 'next_cursor': None, 'has_more': False}
                
                # 정렬 및 제한
                query += " ORDER BY created_at DESC LIMIT $" + str(len(params) + 1)
                params.append(limit + 1)  # 다음 페이지 존재 여부 확인을 위해 1개 더 가져옴
                
                rows = await conn.fetch(query, *params)
                
                # 다음 페이지 존재 여부 확인
                has_more = len(rows) > limit
                if has_more:
                    rows = rows[:-1]  # 마지막 항목 제거
                
                # 다음 커서 생성
                next_cursor = None
                if has_more and rows:
                    next_cursor = rows[-1]['created_at'].isoformat()
                
                chats = [DogChat.from_dict(row) for row in rows]
                
                return {
                    'chats': chats,
                    'next_cursor': next_cursor,
                    'has_more': has_more
                }
                
        except Exception as e:
            logger.error(f"Error getting chats with cursor: {e}")
            return {'chats': [], 'next_cursor': None, 'has_more': False}

    async def get_recent_chats_by_uid(self, uid: str, llm_provider: str = None, limit: int = 10) -> List[DogChat]:
        """사용자 ID로 최근 채팅 이력을 조회합니다."""
        try:
            async with self.pool.acquire() as conn:
                if llm_provider:
                    # llm_provider가 지정된 경우
                    query = """
                        SELECT * FROM dog_chat
                        WHERE uid = $1 AND llm_provider = $2
                        ORDER BY created_at DESC
                        LIMIT $3
                    """
                    results = await conn.fetch(query, uid, llm_provider, limit)
                else:
                    # llm_provider가 None인 경우
                    query = """
                        SELECT * FROM dog_chat
                        WHERE uid = $1
                        ORDER BY created_at DESC
                        LIMIT $2
                    """
                    results = await conn.fetch(query, uid, limit)
                
                return [DogChat.from_dict(dict(row)) for row in results]
        except Exception as e:
            logger.error(f"채팅 이력 조회 중 오류 발생: {str(e)}")
            raise 