from datetime import datetime
from typing import List, Optional
from entity.pulse import Pulse
from entity.measure_pulse import MeasurePulse
import asyncpg

class PulseRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        self.table_name = "t_pulse"
        self.measure_table_name = "t_measure_pulse"

    async def get_by_id(self, idt_pulse: int) -> Optional[Pulse]:
        async with self.pool.acquire() as conn:
            query = f"SELECT * FROM {self.table_name} WHERE idt_pulse = $1"
            result = await conn.fetchrow(query, idt_pulse)
            if result:
                return Pulse(*result)
            return None

    async def get_by_pet_id(self, idt_pet: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT idt_pulse as id, pulse as rate, pulse_dt as measured_at, 'manual' as type
                FROM {self.table_name}
                WHERE idt_pet = $1
                UNION ALL
                SELECT idt_measure_pulse as id, heart_rate as rate, create_dt as measured_at, 'device' as type
                FROM {self.measure_table_name}
                WHERE idt_pet = $2
                ORDER BY measured_at DESC
            """
            results = await conn.fetch(query, idt_pet, idt_pet)
            return [dict(row) for row in results]

    async def get_by_pet_id_and_date(self, idt_pet: int, start_date: datetime) -> List[dict]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT idt_pulse as id, pulse as rate, pulse_dt as measured_at, 'manual' as type
                FROM {self.table_name}
                WHERE idt_pet = $1 AND pulse_dt >= $2
                UNION ALL
                SELECT idt_measure_pulse as id, heart_rate as rate, create_dt as measured_at, 'device' as type
                FROM {self.measure_table_name}
                WHERE idt_pet = $3 AND create_dt >= $4
                ORDER BY measured_at DESC
            """
            results = await conn.fetch(query, idt_pet, start_date, idt_pet, start_date)
            return [dict(row) for row in results]

    async def get_latest_by_pet_id(self, idt_pet: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            query = f"""
                SELECT idt_pulse as id, pulse as rate, pulse_dt as measured_at, 'manual' as type
                FROM {self.table_name}
                WHERE idt_pet = $1
                UNION ALL
                SELECT idt_measure_pulse as id, heart_rate as rate, create_dt as measured_at, 'device' as type
                FROM {self.measure_table_name}
                WHERE idt_pet = $2
                ORDER BY measured_at DESC
                LIMIT 1
            """
            result = await conn.fetchrow(query, idt_pet, idt_pet)
            if result:
                return dict(result)
            return None 