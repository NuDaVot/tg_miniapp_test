import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ChatMemberUpdated
from aiogram.filters import Command, ChatMemberUpdatedFilter

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


# Обработчик добавления бота в новый канал или группу
@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def handle_new_chat_member(event: ChatMemberUpdated):
    try:
        # Проверяем, был ли бот добавлен как администратор
        if event.new_chat_member.status == "administrator":
            chat = event.chat
            chat_type = "канал" if chat.type == "channel" else "группа"
            logger.info(f"Бот добавлен как администратор в {chat_type}: {chat.title} {chat.id}")
            print(f"Бот добавлен как администратор в {chat_type}: {chat.title} {chat.id}")

            # Получение списка администраторов
            admins = await bot.get_chat_administrators(chat.id)
            admin_list = "\n".join([f"- {admin.user.full_name} (@{admin.user.username}) {admin.user.id}"
                                     if admin.user.username else f"- {admin.user.full_name}"
                                     for admin in admins])

            # Вывод информации в консоль
            print(f"Список администраторов {chat_type} '{chat.title}':\n{admin_list}")


    except Exception as e:
        logger.error(f"Ошибка в обработчике добавления бота: {e}")


# Основная функция
async def main():
    # Регистрируем обработчики
    dp.message.register(send_welcome)
    dp.my_chat_member.register(handle_new_chat_member)

    logger.info("Бот запущен...")
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
