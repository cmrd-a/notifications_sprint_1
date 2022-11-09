import asyncio

import aioredis
import backoff

from logger import get_logger
from settings import settings

logger = get_logger(__name__)


@backoff.on_exception(backoff.expo, (aioredis.ConnectionError, AssertionError), logger=logger)
async def wait_redis():
    client = await aioredis.from_url(settings.redis_url)
    assert await client.ping()
    logger.info("connection with redis established")


if __name__ == "__main__":
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(wait_redis())
