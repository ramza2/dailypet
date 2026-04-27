import asyncpg
from typing import List, Optional
import logging
from datetime import datetime
from entity.dog_snack import DogSnack

logger = logging.getLogger(__name__)

class DogSnackRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.table_name = "t_snack"

    async def get_by_id(self, idt_snack: int) -> Optional[DogSnack]:
        try:
            async with self.pool.acquire() as conn:
                query = f"SELECT * FROM {self.table_name} WHERE idt_snack = $1"
                result = await conn.fetchrow(query, idt_snack)
                if result:
                    return DogSnack(*result)
                return None
        except Exception as e:
            logger.error(f"간식 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def get_by_pet_id(self, idt_pet: int, limit: int = 10) -> List[DogSnack]:
        try:
            async with self.pool.acquire() as conn:
                query = f"""
                    SELECT * FROM {self.table_name}
                    WHERE idt_pet = $1
                    ORDER BY snack_date DESC
                    LIMIT $2
                """
                results = await conn.fetch(query, idt_pet, limit)
                return [DogSnack(*row) for row in results]
        except Exception as e:
            logger.error(f"반려견 간식 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 

    async def get_by_pet_id_and_date(self, idt_pet: int, start_date: datetime) -> List[DogSnack]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE idt_pet = $1 AND snack_date >= $2
                ORDER BY snack_date DESC
            """
            results = await conn.fetch(query, idt_pet, start_date)
            return [DogSnack(*row) for row in results] 