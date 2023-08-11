from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import executor

from core import Bot
from middlewares import SemaphoreMiddleware, CounterMiddleware
from settings import Settings

config = Settings.load("config.yml")
bot = Bot(config.API_TOKEN, parse_mode="html")
bot.middleware(SemaphoreMiddleware(), CounterMiddleware())
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def startCommand(message: Message):
    await message.answer("Hello!")


if __name__ == "__main__":
    from logging import basicConfig, INFO

    basicConfig(level=INFO)

    executor.start_polling(dp)
