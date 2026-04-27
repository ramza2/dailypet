import asyncpg
from typing import List, Optional
import logging
from datetime import datetime
from entity.dog_walk import DogWalk

logger = logging.getLogger(__name__)

class DogWalkRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.table_name = "t_walk"

    async def get_by_id(self, idt_walk: int) -> Optional[DogWalk]:
        try:
            async with self.pool.acquire() as conn:
                query = f"SELECT * FROM {self.table_name} WHERE idt_walk = $1"
                result = await conn.fetchrow(query, idt_walk)
                if result:
                    return DogWalk(*result)
                return None
        except Exception as e:
            logger.error(f"산책 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def get_by_pet_id(self, idt_pet: int, limit: int = 10) -> List[DogWalk]:
        try:
            async with self.pool.acquire() as conn:
                query = f"""
                    SELECT * FROM {self.table_name}
                    WHERE idt_pet = $1
                    ORDER BY walk_dt DESC
                    LIMIT $2
                """
                results = await conn.fetch(query, idt_pet, limit)
                return [DogWalk(*row) for row in results]
        except Exception as e:
            logger.error(f"반려견 산책 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def get_by_pet_id_and_date(self, idt_pet: int, start_date: datetime) -> List[DogWalk]:
        async with self.pool.acquire() as conn:
            # datetime을 'YYYY-MM-DD' 형식의 문자열로 변환
            start_date_str = start_date.strftime('%Y-%m-%d')
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE idt_pet = $1 AND walk_dt >= $2
                ORDER BY walk_dt DESC
            """
            results = await conn.fetch(query, idt_pet, start_date_str)
            return [DogWalk(*row) for row in results]

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 