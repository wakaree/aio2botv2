import functools
from asyncio import BaseEventLoop, AbstractEventLoop
from typing import Optional, Dict, Any, Union, List, Callable

from aiogram import Bot as _Bot
from aiogram.bot.api import TelegramAPIServer, TELEGRAM_PRODUCTION
from aiogram.types import base
from aiohttp import BasicAuth, ClientTimeout

from .manager import RequestManager
from .request_middleware import BaseRequestMiddleware


class Bot(_Bot):
    def __init__(
        self,
        token: base.String,
        loop: Optional[Union[BaseEventLoop, AbstractEventLoop]] = None,
        connections_limit: Optional[base.Integer] = None,
        proxy: Optional[base.String] = None,
        proxy_auth: Optional[BasicAuth] = None,
        validate_token: Optional[base.Boolean] = True,
        parse_mode: Optional[base.String] = None,
        disable_web_page_preview: Optional[base.Boolean] = None,
        protect_content: Optional[base.Boolean] = None,
        timeout: Optional[Union[base.Integer, base.Float, ClientTimeout]] = None,
        server: TelegramAPIServer = TELEGRAM_PRODUCTION,
    ):
        super().__init__(
            token=token,
            loop=loop,
            connections_limit=connections_limit,
            proxy=proxy,
            proxy_auth=proxy_auth,
            validate_token=validate_token,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            protect_content=protect_content,
            timeout=timeout,
            server=server,
        )

        self.manager = RequestManager(self, self._token)
        self.middlewares: List[BaseRequestMiddleware] = []

    def middleware(self, *middlewares: BaseRequestMiddleware) -> None:
        self.middlewares.extend(middlewares)

    def wrap_middlewares(self, callback: Callable[..., Any]) -> Any:
        @functools.wraps(callback)
        def _wrapper(*args: Any) -> Any:
            return callback(*args)

        for m in reversed(self.middlewares):
            _wrapper = functools.partial(m, _wrapper)

        return _wrapper

    async def request(
        self,
        method: base.String,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        **kwargs: Any
    ) -> Any:
        callback = self.wrap_middlewares(self.manager)
        return await callback(method, data, files, **kwargs)
