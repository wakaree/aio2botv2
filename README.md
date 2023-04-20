# aio2botv2
Бот на aiogram 2 с возможностью установки мидлварей (промежуточных программ) на исходящие запросы из бота.  
  
**Вся логика находится [тут](https://github.com/wakaree/aio2botv2/blob/main/_bot)**  
**Примеры находятся [тут](https://github.com/wakaree/aio2botv2/blob/main/middlewares)**  
  
**Установка:**  
  
```
from aiogram import Dispatcher

from _bot import BotV2
from middlewares import YourMiddlewareExample, YourMiddlewareExample2

bot = BotV2("token")
bot.middleware(YourMiddlewareExample(), YourMiddlewareExample2())
dp = Dispatcher(bot)
```
  
  
надеюсь, кому-нибудь это будет полезно..  
