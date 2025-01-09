from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

# Укажите свой токен Telegram Bot API
BOT_TOKEN = os.getenv('TECHSUPPORT_BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Создаем кнопку с Mini App
    web_app = WebAppInfo(url="https://your-miniapp-url.com")  # Укажите URL вашего Mini App
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Открыть список каналов", web_app=web_app)
    )
    await message.answer("Нажмите кнопку ниже, чтобы открыть список каналов:", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
