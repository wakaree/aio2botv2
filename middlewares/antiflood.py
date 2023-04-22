
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Union

from aiogram.types import Message, ChatPermissions
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):
    DEFAULT_WARNING_LIMIT = 3
    DEFAULT_HARD_LIMIT = 6
    DEFAULT_TTL = 3
    DEFAULT_MUTE_TIME = 3600

    def __init__(
        self,
        warning_limit: int = DEFAULT_WARNING_LIMIT,
        hard_limit: int = DEFAULT_HARD_LIMIT,
        ttl: Union[int, float] = DEFAULT_TTL,
        mute_time: int = DEFAULT_MUTE_TIME
    ):
        self.warning_limit = warning_limit
        self.hard_limit = hard_limit
        self.mute_time = timedelta(seconds=mute_time)
        self.enabled = False

        self._cache = TTLCache(maxsize=10_000, ttl=ttl)

        super().__init__()

    async def on_pre_process_message(self, event: Message, data: Dict):  # noqa
        if self.enabled and event.chat.type == "supergroup":
            if event.from_user.id not in self._cache:
                self._cache[event.from_user.id] = 1

            else:
                self._cache[event.from_user.id] += 1

            if self._cache[event.from_user.id] >= self.hard_limit:
                until = datetime.now() + self.mute_time

                await event.chat.restrict(
                    event.from_user.id,
                    ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_polls=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_manage_topics=False
                    ),
                    until
                )
                await event.reply(f"You are not allowed to chat until {until}.")

                del self._cache[event.from_user.id]
                raise CancelHandler()

            elif self._cache[event.from_user.id] >= self.warning_limit:
                await event.reply(
                    "If you do not stop flooding, "
                    "I will be forced to restrict you of the right to write to the chat."
                )
