# aio2botv2
Бот на aiogram 2 с возможностью установки мидлварей (промежуточных программ) на исходящие запросы из бота.

**Вся логика находится в ./_bot**
**Примеры мидлварей находятся в ./middlewares**


Пример мидлваря "счётчик исходящих запросов" (**ссылка на код**)[./middlewares/counter]:

```
class CounterMiddleware(BaseRequestMiddleware):
    def __init__(self):
        self.counters = {counter: 0 for counter in Methods.all()}

    async def __call__(
        self, request: RequestManager, method: str,
        data: Any = None, files: Any = None, **kwargs: Any
    ) -> Response:
        self.counters[method] += 1

        return await request(method, data, files, **kwargs)
```

**Установка ничем не отличается от обычной настройки бота в aiogram2.**

```
from _bot import BotV2
from middlewares import YourMiddlewareExample, YourMiddlewareExample2

bot = BotV2("token")
bot.middleware(YourMiddlewareExample(), YourMiddlewareExample2())
dp = Dispatcher(bot)
```

надеюсь, кому-нибудь это будет полезно..
