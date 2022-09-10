from aiogram.types import Message
from config import admin_erikk_id
from main import bot, dp


# Функция, которая будет отправлять сообщение админу при старте
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_erikk_id, text='Бот запущен! Введите /start')


@dp.message_handler()
async def echo(message: Message):
    text = f"🙈 У нас нет такой команды: '{message.text}'"
    await message.answer(text=text)  # Ответ_2

