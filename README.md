# aio2botv2
aiogram v2.25.1 bot with the ability to install middlewares for outgoing requests from the bot.
  
**Middlewares logic is [here](https://github.com/wakaree/aio2botv2/blob/main/core)**  
**Examples is [here](https://github.com/wakaree/aio2botv2/blob/main/middlewares)**  
  
**MRE:**
```python
import asyncio
from logging import basicConfig, INFO

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from core import Bot
from middlewares import CounterMiddleware


async def start_command(message: Message) -> None:
    await message.answer("Hello!")


async def main() -> None:
    basicConfig(level=INFO)

    bot = Bot("42:ABC", parse_mode="html")
    bot.middleware(CounterMiddleware())

    dp = Dispatcher(bot)
    dp.register_message_handler(start_command, CommandStart())

    try:
        await dp.start_polling()
    finally:
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
```