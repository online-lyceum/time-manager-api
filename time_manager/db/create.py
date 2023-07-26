import asyncio
import logging

import asyncpg
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    postgres_host: str = 'postgres'
    postgres_db: str = 'db'
    postgres_password: str = 'password'
    postgres_user: str = 'postgres'


settings = Settings()


async def connect_create_if_not_exists(user, database, password, host):
    try:
        conn = await asyncpg.connect(user=user, database=database,
                                     password=password, host=host)
        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user='postgres',
            password=password,
            host=host
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"'
        )
        await sys_conn.close()


def run_init_db():
    asyncio.run(connect_create_if_not_exists(
        settings.postgres_user,
        settings.postgres_db,
        settings.postgres_password,
        settings.postgres_host))
    logger.info('DB initialization is done')
