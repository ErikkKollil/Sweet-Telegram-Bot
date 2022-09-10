import os
import keybordsbot as kb

from aiogram.dispatcher.filters import Command
from aiogram import types
from main import bot, dp
from DataBase_PostgreSQL.main_bd_postgre import execute_contact, checkin_contact
from config import admin_erikk_id, admin_daria_id

# Загружаем библиотеку с ценами
path_price = os.path.join(os.getcwd(), 'Price')
photos = [os.path.join(path_price, file) for file in os.listdir(path_price)]


# Первое сообщение после нажатия на start и вывод кнопок
@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    await message.answer("Ознакомьтесь с меню ниже 👇🏻", reply_markup=kb.menu)


# Выводим информацию об авторе
@dp.message_handler(text="Об авторе 👩‍🍳")
async def get_about(message: types.Message):
    await message.answer("Я - Дарья! 👩‍🍳 Начинающий кондитер!\n"
                         "Связаться со мной вы можете здесь 🌸\n", reply_markup=kb.inline_kb_links)


# Выводим примеры
@dp.message_handler(text="Примеры работ 🧁")
async def get_about(message: types.Message):
    await bot.send_photo(message.from_user.id, open('Examples/ch_keks.jpg', 'rb'))
    await message.answer("Ознакомьтесь с примерами 👇🏻", reply_markup=kb.inline_kb_represent)


# Выводим все файлы с ценами (Price)
@dp.message_handler(text="Прайс 🧾")
async def get_about(message: types.Message):
    for ph in photos:
        await bot.send_photo(message.from_user.id, open(ph, 'rb'))


# Выводим примеры
@dp.message_handler(text="Условия заказа и доставка 📦")
async def get_about(message: types.Message):
    await bot.send_photo(message.from_user.id, open('Terms/usl.jpg', 'rb'))
    await bot.send_photo(message.from_user.id, open('Terms/dost.jpg', 'rb'))


# Забираем данные пользователя, которыми он поделился с нами (контакты)
# И сообщаем администраторам о новом запросе на звонок
@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:
        if not checkin_contact(message.contact.user_id):
            execute_contact(message.contact.user_id, message.contact.first_name, '+' + message.contact.phone_number)
            await message.answer("Ваше обращение зарегистрировано 🌸")

            texts = f"🔥 Новый запрос на звонок 🔥\nNickname: {message.contact.first_name}" \
                    f"\nName profile: @{message.chat.username}" \
                    f"\nPhone number: +{message.contact.phone_number}"

            await bot.send_message(chat_id=admin_erikk_id, text=texts)
            await bot.send_message(chat_id=admin_daria_id, text=texts)
        else:
            await message.answer("Вы уже оставляли обращение ранее 🌸\n"
                                 "Дарья помнит о вас и скоро свяжется 🌸")
