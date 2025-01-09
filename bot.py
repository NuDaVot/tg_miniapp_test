from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio

# Укажите токен вашего бота
BOT_TOKEN = ""

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик для приема данных из WebApp
@dp.message(F.content_type == "web_app_data")
async def handle_web_app_data(message: Message):
    # Логирование сообщения
    print(json.dumps(message.json(), indent=4, ensure_ascii=False))

    if message.web_app_data:
        data = message.web_app_data.data
        await message.reply(f"Получены данные из WebApp: {data}")
    else:
        await message.reply("Данные из WebApp не переданы.")


# Основная функция запуска
async def main():
    # Регистрируем обработчики
    dp.message.register(handle_web_app_data)

    # Запускаем поллинг
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == "__main__":
    asyncio.run(main())
