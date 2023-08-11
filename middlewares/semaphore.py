from asyncio import Semaphore
from logging import getLogger
from typing import Any

from aiogram.bot.api import Methods

from core import BaseRequestMiddleware, Response
from core.manager import RequestManager


class SemaphoreMiddleware(BaseRequestMiddleware):
    RATE_LIMIT = 25

    def __init__(self, rate_limit: int = RATE_LIMIT):
        self.semaphores = {method: Semaphore(rate_limit) for method in Methods.all()}
        self.log = getLogger(__name__)

    async def __call__(
        self,
        request: RequestManager,
        method: str,
        data: Any = None,
        files: Any = None,
        **kwargs: Any
    ) -> Response:
        async with self.semaphores[method]:
            return await request(method, data, files, **kwargs)
