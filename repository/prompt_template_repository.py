import asyncpg
from typing import List, Optional
import logging
from datetime import datetime
from entity.prompt_template import PromptTemplate

logger = logging.getLogger(__name__)

class PromptTemplateRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create(self, template: PromptTemplate) -> int:
        """새로운 프롬프트 템플릿을 생성합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                INSERT INTO prompt_template (name, content, created_at)
                VALUES ($1, $2, $3)
                RETURNING id
                """
                result = await conn.fetchval(
                    query,
                    template.name,
                    template.content,
                    template.created_at
                )
                return result
        except Exception as e:
            logger.error(f"프롬프트 템플릿 생성 중 오류 발생: {str(e)}")
            raise

    async def get_by_id(self, template_id: int) -> Optional[PromptTemplate]:
        """ID로 프롬프트 템플릿을 조회합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT id, name, content, created_at, updated_at
                FROM prompt_template
                WHERE id = $1
                """
                row = await conn.fetchrow(query, template_id)
                return PromptTemplate.from_dict(dict(row)) if row else None
        except Exception as e:
            logger.error(f"프롬프트 템플릿 조회 중 오류 발생: {str(e)}")
            raise

    async def get_all(self) -> List[PromptTemplate]:
        """모든 프롬프트 템플릿을 조회합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                SELECT id, name, content, created_at, updated_at
                FROM prompt_template
                ORDER BY created_at DESC
                """
                rows = await conn.fetch(query)
                return [PromptTemplate.from_dict(dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"프롬프트 템플릿 목록 조회 중 오류 발생: {str(e)}")
            raise

    async def update(self, template: PromptTemplate) -> bool:
        """프롬프트 템플릿을 수정합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                UPDATE prompt_template
                SET name = $1, content = $2, updated_at = $3
                WHERE id = $4
                """
                result = await conn.execute(
                    query,
                    template.name,
                    template.content,
                    datetime.now(),
                    template.id
                )
                return result == "UPDATE 1"
        except Exception as e:
            logger.error(f"프롬프트 템플릿 수정 중 오류 발생: {str(e)}")
            raise

    async def delete(self, template_id: int) -> bool:
        """프롬프트 템플릿을 삭제합니다."""
        try:
            async with self.pool.acquire() as conn:
                query = "DELETE FROM prompt_template WHERE id = $1"
                result = await conn.execute(query, template_id)
                return result == "DELETE 1"
        except Exception as e:
            logger.error(f"프롬프트 템플릿 삭제 중 오류 발생: {str(e)}")
            raise 