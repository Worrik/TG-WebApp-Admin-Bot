import asyncpg
from asyncpg.pool import Pool

class DB:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def add_user(self, name: str, telegram_id: int):
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                'select * from users where telegram_id = $1',
                telegram_id
            )
            if not user:
                await conn.execute(
                    'insert into users (name, telegram_id) values ($1, $2)',
                    name, telegram_id
                )
            else:
                await conn.execute(
                    'update users set name = $1 where telegram_id = $2',
                    name, telegram_id
                )

    async def delete_user_data(self, telegram_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                'delete from users where telegram_id = $1',
                telegram_id
            )

    @classmethod
    async def create(cls, DATABASE_URL: str):
        pool = await asyncpg.create_pool(DATABASE_URL)
        if pool:
            return cls(pool)

