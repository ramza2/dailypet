import asyncpg
from typing import List, Optional
import logging
from datetime import datetime
from entity.dog_meal import DogMeal

logger = logging.getLogger(__name__)

class DogMealRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.table_name = "t_feed"

    async def get_by_id(self, idt_feed: int) -> Optional[DogMeal]:
        try:
            async with self.pool.acquire() as conn:
                query = f"SELECT * FROM {self.table_name} WHERE idt_feed = $1"
                result = await conn.fetchrow(query, idt_feed)
                if result:
                    return DogMeal(*result)
                return None
        except Exception as e:
            logger.error(f"식사 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def get_by_pet_id(self, idt_pet: int, limit: int = 10) -> List[DogMeal]:
        try:
            async with self.pool.acquire() as conn:
                query = f"""
                    SELECT * FROM {self.table_name}
                    WHERE idt_pet = $1
                    ORDER BY feed_dt DESC
                    LIMIT $2
                """
                results = await conn.fetch(query, idt_pet, limit)
                return [DogMeal(*row) for row in results]
        except Exception as e:
            logger.error(f"반려견 식사 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 

    async def get_by_pet_id_and_date(self, idt_pet: int, start_date: datetime) -> List[DogMeal]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE idt_pet = $1 AND feed_dt >= $2
                ORDER BY feed_dt DESC
            """
            results = await conn.fetch(query, idt_pet, start_date)
            return [DogMeal(*row) for row in results] 