from typing import Any

from core import BaseRequestMiddleware, Response
from core.manager import RequestManager


class CounterMiddleware(BaseRequestMiddleware):
    def __init__(self):
        self.counters = {}

    async def __call__(
        self,
        request: RequestManager,
        method: str,
        data: Any = None,
        files: Any = None,
        **kwargs: Any
    ) -> Response:
        if method not in self.counters:
            self.counters[method] = 0
        self.counters[method] += 1
        return await request(method, data, files, **kwargs)
