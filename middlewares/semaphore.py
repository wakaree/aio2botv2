
from asyncio import Semaphore, sleep as asleep
from logging import getLogger
from typing import Any

from aiogram.bot.api import Methods
from aiogram.utils.exceptions import RetryAfter

from _bot import BaseRequestMiddleware
from _bot.manager import RequestManager


class SemaphoreMiddleware(BaseRequestMiddleware):
    RATE_LIMIT = 25

    def __init__(self, rate_limit: int = RATE_LIMIT):
        self.semaphores = {method: Semaphore(rate_limit) for method in Methods.all()}
        self.log = getLogger(__name__)

    async def __call__(
        self, request: RequestManager, method: str,
        data: Any = None, files: Any = None, **kwargs: Any
    ):
        async with self.semaphores[method]:
            return await request(method, data, files, **kwargs)
