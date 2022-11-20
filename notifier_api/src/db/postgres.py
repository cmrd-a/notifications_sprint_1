from psycopg2.extensions import connection

pg: connection | None = None


async def get_postgres() -> connection | None:
    return pg
