import asyncpg
from typing import List, Optional
import logging
from datetime import datetime
from entity.dog_temperature import DogTemperature

logger = logging.getLogger(__name__)

class DogTemperatureRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.table_name = "t_temperature"

    async def get_by_id(self, idt_temperature: int) -> Optional[DogTemperature]:
        try:
            async with self.pool.acquire() as conn:
                query = f"SELECT * FROM {self.table_name} WHERE idt_temperature = $1"
                result = await conn.fetchrow(query, idt_temperature)
                if result:
                    return DogTemperature(*result)
                return None
        except Exception as e:
            logger.error(f"체온 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def get_by_pet_id(self, idt_pet: int, limit: int = 10) -> List[DogTemperature]:
        try:
            async with self.pool.acquire() as conn:
                query = f"""
                    SELECT * FROM {self.table_name}
                    WHERE idt_pet = $1
                    ORDER BY temp_dt DESC
                    LIMIT $2
                """
                results = await conn.fetch(query, idt_pet, limit)
                return [DogTemperature(*row) for row in results]
        except Exception as e:
            logger.error(f"반려견 체온 기록 조회 중 오류 발생: {str(e)}")
            raise

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨

    async def get_by_pet_id_and_date(self, idt_pet: int, start_date: datetime) -> List[DogTemperature]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE idt_pet = $1 AND temp_dt >= $2
                ORDER BY temp_dt DESC
            """
            results = await conn.fetch(query, idt_pet, start_date)
            return [DogTemperature(*row) for row in results]