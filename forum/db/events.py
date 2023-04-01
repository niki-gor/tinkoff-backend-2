import asyncpg
from fastapi import FastAPI
from loguru import logger

from forum.core.settings import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        str(settings.dsn),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
