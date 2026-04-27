import asyncpg
from typing import List, Optional
from datetime import datetime
from entity.user import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_user(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO t_user (
                    uid, push_key, id, phone, thumb_type, thumb_content,
                    name, address, deleted, name_changed_dt, create_dt
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                RETURNING *
                """,
                user.uid, user.push_key, user.id, user.phone,
                user.thumb_type, user.thumb_content, user.name,
                user.address, user.deleted, user.name_changed_dt,
                user.create_dt or datetime.now()
            )
            return User.from_dict(dict(row))

    async def get_user(self, uid: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM t_user
                WHERE uid = $1 AND deleted = false
                """,
                uid
            )
            return User.from_dict(dict(row)) if row else None

    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM t_user
                WHERE phone = $1 AND deleted = false
                """,
                phone
            )
            return User.from_dict(dict(row)) if row else None

    async def update_user(self, user: User) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE t_user
                SET push_key = $1, thumb_type = $2, thumb_content = $3,
                    name = $4, address = $5, name_changed_dt = $6
                WHERE uid = $7 AND deleted = false
                RETURNING *
                """,
                user.push_key, user.thumb_type, user.thumb_content,
                user.name, user.address, datetime.now(), user.uid
            )
            return User.from_dict(dict(row)) if row else None

    async def delete_user(self, uid: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE t_user
                SET deleted = true
                WHERE uid = $1
                """,
                uid
            )
            return result == "UPDATE 1"

    async def close(self):
        """리소스 정리"""
        pass  # pool은 FastAPI lifespan에서 관리됨 