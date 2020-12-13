import asyncio
import asyncpg
from injector import inject, singleton


@singleton
class AsyncPostgresClient:
    @inject
    def __init__(self, address: str):
        self.address = address

    def __str__(self):
        return f"AsyncPostgresClient: {self.address}"

    async def select(self, query):
        connection = await asyncpg.connect(dsn=self.address)
        result = await connection.fetch(query)
        await connection.close()
        return [dict(res) for res in result] if result else None

    async def select_one_value(self, query):
        connection = await asyncpg.connect(dsn=self.address)
        result = await connection.fetch(query)
        await connection.close()
        return result[0][0] if result else None

    async def execute(self, query):
        connection = await asyncpg.connect(dsn=self.address)
        result = None
        async with connection.transaction():
            result = await connection.execute(query)
        await connection.close()
        #print(result)
        return result if result else None


