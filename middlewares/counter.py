from typing import Any

from aiogram.bot.api import Methods

from _bot import BaseRequestMiddleware, Response
from _bot.manager import RequestManager


class CounterMiddleware(BaseRequestMiddleware):
    def __init__(self):
        self.counters = {counter: 0 for counter in Methods.all()}

    async def __call__(
        self, request: RequestManager, method: str,
        data: Any = None, files: Any = None, **kwargs: Any
    ) -> Response:
        self.counters[method] += 1

        return await request(method, data, files, **kwargs)
