import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные из .env
load_dotenv()

# Укажите ваш токен Telegram Bot API
BOT_TOKEN = os.getenv('BOT_TOKEN')
URL_MINIAPP = os.getenv('URL_MINIAPP')

# Проверяем, что переменные загружены
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
if not URL_MINIAPP:
    raise ValueError("Переменная окружения URL_MINIAPP не задана!")

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    try:
        # Создаем кнопку с Mini App
        web_app = WebAppInfo(url=URL_MINIAPP)  # Укажите URL вашего Mini App
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть список каналов", web_app=web_app)]
        ])
        await message.answer("Нажмите кнопку ниже, чтобы открыть список каналов:", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Основная функция
async def main():
    # Регистрируем обработчики
    dp.message.register(send_welcome)

    logger.info("Бот запущен...")
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
