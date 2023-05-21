
from abc import ABC, abstractmethod
from typing import Any

from .response import Response
from .manager import RequestManager


class BaseRequestMiddleware(ABC):
    @abstractmethod
    async def __call__(
        self, request: RequestManager, method: str,
        data: Any = None, files: Any = None, **kwargs: Any
    ) -> Response:
        ...
