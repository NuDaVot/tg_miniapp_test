from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token="7394837810:AAHPnLmy6AD_n7fmX3wpBjNjeqtYS1AKza4")
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_web_app_data(message: types.Message):
    user_data = message.web_app_data.data
    user_id = user_data.get("user_id")
    username = user_data.get("username")

    # Список чатов, где бот является администратором
    chat_admins = []

    # Получение чатов, где бот добавлен
    async for chat in bot.get_updates():
        try:
            # Проверяем права администратора для каждого чата
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status in ['administrator', 'creator']:
                chat_admins.append(chat.title)
        except Exception as e:
            continue

    # Отправка результата пользователю
    if chat_admins:
        await message.answer(f"Вы администратор в следующих чатах:\n" + "\n".join(chat_admins))
    else:
        await message.answer("Вы не являетесь администратором ни в одном чате.")
