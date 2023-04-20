import functools
from asyncio import BaseEventLoop, AbstractEventLoop
from typing import Optional, Dict, Any, Union, List

from aiogram import Bot
from aiogram.bot.api import TelegramAPIServer, TELEGRAM_PRODUCTION
from aiogram.types import base
from aiohttp import BasicAuth, ClientTimeout

from .manager import RequestManager
from .request_middleware import BaseRequestMiddleware


class BotV2(Bot):
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
        server: TelegramAPIServer = TELEGRAM_PRODUCTION
    ):
        self.__token = token

        super().__init__(
            self.__token, loop, connections_limit, proxy, proxy_auth,
            validate_token, parse_mode, disable_web_page_preview,
            protect_content, timeout, server
        )

        self.manager = RequestManager(self, self.__token)
        self.middlewares: Optional[List[BaseRequestMiddleware]] = []

    def middleware(self, *middlewares: BaseRequestMiddleware) -> None:
        self.middlewares.extend(middlewares)

    def wrap_middlewares(self, callback: callable) -> Any:
        @functools.wraps(callback)
        def _wrapper(*args: Any) -> Any:
            return callback(*args)

        for m in reversed(self.middlewares):
            _wrapper = functools.partial(m, _wrapper)

        return _wrapper

    async def request(
        self, method: base.String, data: Optional[Dict] = None,
        files: Optional[Dict] = None, **kwargs
    ) -> Any:
        call = self.wrap_middlewares(self.manager)

        return await call(method, data, files, **kwargs)
