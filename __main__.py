
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

from _bot import BotV2
from settings import Settings
from middlewares import (
    SemaphoreMiddleware, CounterMiddleware,
    AntiFloodMiddleware
)


config = Settings.load('config.yml')
bot = BotV2(config.API_TOKEN, parse_mode='html')
bot.middleware(SemaphoreMiddleware(), CounterMiddleware())
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def startCommand(message: Message):
    await message.answer("Hello!")


if __name__ == '__main__':
    from logging import basicConfig, INFO
    basicConfig(level=INFO)

    dp.setup_middleware(AntiFloodMiddleware())
    executor.start_polling(dp)
