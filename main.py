import asyncio  # Для работы с асинхронными функциями
import menu     # Для работы с меню

from DataBase_PostgreSQL.main_bd_postgre import execute_comment
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types
from config import bot_token, admin_daria_id, admin_erikk_id

# Поток в котором будут обрабатываться все события
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
storage = MemoryStorage()

bot = Bot(bot_token, parse_mode='HTML')  # Создали экземпляр класса Бота
dp = Dispatcher(bot, loop=loop, storage=storage)


# Машина состояний
class UserState(StatesGroup):
    fullname = State()
    comment = State()


@dp.message_handler(text="Оставить отзыв 💬")
async def get_about(message: types.Message):
    await message.answer("🌸 Введите своё имя 🌸")
    await UserState.fullname.set()


# Передали state: FSMContext для того, чтобы мы могли записывать данные пользователя в память
@dp.message_handler(state=UserState.fullname)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(my_nickname=message.text)
    await message.answer("Отлично! 🌸 Теперь напишите Ваш отзыв")
    await UserState.next()  # либо же UserState.address.set()


@dp.message_handler(state=UserState.comment)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(my_comment=message.text)

    data_comment = await state.get_data()
    await message.answer(f"🌸 Ваш отзыв зарегистрирован 🌸\n"
                         f"Ваше имя: {data_comment['my_nickname']}\n"
                         f"Ваш отзыв: {data_comment['my_comment']}")

    execute_comment(message.from_user.id, message.from_user.first_name, message.from_user.username,
                    data_comment['my_nickname'], data_comment['my_comment'])

    text_comment = f"🍰 Новый отзыв 🍰\nИмя пользователя: {data_comment['my_nickname']}" \
                   f"\nЕго отзыв: '{data_comment['my_comment']}'"

    await bot.send_message(chat_id=admin_erikk_id, text=text_comment)
    await bot.send_message(chat_id=admin_daria_id, text=text_comment)
    await state.finish()


if __name__ == "__main__":
    print("[INFO+] Bot started!")
    from handlers import dp, send_to_admin

    executor.start_polling(dp, on_startup=send_to_admin)  # Доставляет сообщения при старте
