import asyncio
from logging import basicConfig, INFO

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from core import Bot
from middlewares import CounterMiddleware
from settings import Settings


async def start_command(message: Message) -> None:
    await message.answer("Hello!")


async def main() -> None:
    basicConfig(level=INFO)
    config = Settings.load("config.yml")

    bot = Bot(config.API_TOKEN, parse_mode="html")
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
