import asyncpg
from typing import List, Optional
from datetime import datetime
from entity.pet import Pet
import logging

logger = logging.getLogger(__name__)

class PetRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_pet(self, pet: Pet) -> Pet:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO t_pet (
                    uid, name, thumb_type, thumb_content, gender, neutering_yn,
                    birthday, adoption_date, breed, weight, classification,
                    regist_number, deleted, create_dt,
                    bcs_type, health_status, health_issues, last_checkup_date
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
                RETURNING *
                """,
                pet.uid, pet.name, pet.thumb_type, pet.thumb_content,
                pet.gender, pet.neutering_yn, pet.birthday, pet.adoption_date,
                pet.breed, pet.weight, pet.classification, pet.regist_number,
                pet.deleted, pet.create_dt or datetime.now(),
                pet.bcs_type, pet.bcs_score, pet.health_status, pet.health_issues, pet.last_checkup_date
            )
            return Pet.from_dict(dict(row))

    async def get_pet(self, idt_pet: int) -> Optional[Pet]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT *, bcs_type, health_status, health_issues, last_checkup_date FROM t_pet
                WHERE idt_pet = $1 AND deleted = false
                """,
                idt_pet
            )
            return Pet.from_dict(dict(row)) if row else None

    async def get_pets_by_user(self, uid: str) -> List[Pet]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT *, bcs_type, health_status, health_issues, last_checkup_date FROM t_pet
                WHERE uid = $1 AND deleted = false
                ORDER BY create_dt DESC
                """,
                uid
            )
            return [Pet.from_dict(dict(row)) for row in rows]
        
    async def get_all_pets(self) -> List[Pet]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT *, bcs_type, health_status, health_issues, last_checkup_date FROM t_pet
                WHERE deleted = false
                ORDER BY create_dt DESC
                """
            )
            return [Pet.from_dict(dict(row)) for row in rows]

    async def update_pet(self, pet: Pet) -> Optional[Pet]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE t_pet
                SET name = $1, thumb_type = $2, thumb_content = $3,
                    gender = $4, neutering_yn = $5, birthday = $6,
                    adoption_date = $7, breed = $8, weight = $9,
                    classification = $10, regist_number = $11,
                    bcs_type = $12, health_status = $13, health_issues = $14, last_checkup_date = $15
                WHERE idt_pet = $16 AND deleted = false
                RETURNING *
                """,
                pet.name, pet.thumb_type, pet.thumb_content,
                pet.gender, pet.neutering_yn, pet.birthday,
                pet.adoption_date, pet.breed, pet.weight,
                pet.classification, pet.regist_number,
                pet.bcs_type, pet.health_status, pet.health_issues, pet.last_checkup_date,
                pet.idt_pet
            )
            return Pet.from_dict(dict(row)) if row else None

    async def delete_pet(self, idt_pet: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE t_pet
                SET deleted = true
                WHERE idt_pet = $1
                """,
                idt_pet
            )
            return result == "UPDATE 1"

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 