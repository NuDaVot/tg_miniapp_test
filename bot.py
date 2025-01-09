import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Укажите ваш токен Telegram Bot API
BOT_TOKEN = os.getenv('BOT_TOKEN')
URL_MINIAPP = os.getenv('URL_MINIAPP')

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def send_welcome(message: Message):
    # Создаем кнопку с Mini App
    web_app = WebAppInfo(url=URL_MINIAPP)  # Укажите URL вашего Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть список каналов", web_app=web_app)]
    ])
    await message.answer("Нажмите кнопку ниже, чтобы открыть список каналов:", reply_markup=keyboard)

async def main():
    # Регистрируем обработчики
    dp.message.register(send_welcome)
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
