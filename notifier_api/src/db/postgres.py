from psycopg import AsyncConnection

pg: AsyncConnection | None = None


async def get_postgres() -> AsyncConnection | None:
    return pg
