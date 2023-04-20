
from abc import abstractmethod
from typing import Any

from .response import Response
from .manager import RequestManager


class BaseRequestMiddleware:
    @abstractmethod
    async def __call__(
        self, request: RequestManager, method: str,
        data: Any = None, files: Any = None, **kwargs: Any
    ) -> Response:
        raise NotImplementedError(
            f'{self.__class__.__name__} must implement __call__ method!'
        )
