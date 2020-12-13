import asyncio
from tools.asyncio_postgres_client import AsyncPostgresClient



def query_insert_new_task(data):
    query_string = """
        INSERT INTO tasks (
            initial_url, max_depth
            )
        VALUES (
        '{initial_url}'::text,
        '{max_depth}'::integer
        )
        ON CONFLICT DO NOTHING
        RETURNING *;
    """
    return query_string.format(**data)

def query_get_task_id(data):
    query_string = """
        SELECT task_id
        FROM tasks
        WHERE max_depth='{max_depth}'::integer AND initial_url LIKE '{initial_url}'::text
    """
    return query_string.format(**data)

class PG:
    def __init__(self):
        self.pg_client = AsyncPostgresClient("")
        self.queries = {
            "query_insert_new_task": query_insert_new_task,
            
            "query_get_task_id": query_get_task_id,
            
        }


    async def get_task_id(self, initial_url, max_depth):
        data = {
            "initial_url": initial_url,
            "max_depth": max_depth,
        }
        await self.pg_client.execute(self.queries["query_insert_new_task"](data))
        
        return await self.pg_client.select_one_value(self.queries["query_get_task_id"](data))
        


