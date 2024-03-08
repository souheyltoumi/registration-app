from dao.conf.model_settings import get_settings
import asyncpg

settings = get_settings()


async def admin_dbh() -> asyncpg.Connection:
    conn = await asyncpg.connect(str(settings.db['admin'].dsn))
    try:
        yield conn
    finally:
        await conn.close()
