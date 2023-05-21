
from typing import Any

from aiogram import Bot
from aiogram.bot.api import make_request

from .response import Response


class RequestManager:
    def __init__(self, bot: Bot, token: str):
        self.bot = bot
        self.__token = token

    async def __call__(self, method: str, data: Any = None, files: Any = None, **kwargs) -> Response:
        session = await self.bot.get_session()

        return await make_request(
            session, self.bot.server, self.__token, method, data, files,
            proxy=self.bot.proxy, proxy_auth=self.bot.proxy_auth, timeout=self.bot.timeout, **kwargs
        )
