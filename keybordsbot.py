from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import link_telegram, link_vk, link_instagram, link_whatsapp

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Об авторе 👩‍🍳'),
            KeyboardButton(text='Примеры работ 🧁')
        ],
        [
            KeyboardButton(text='Прайс 🧾'),
            KeyboardButton(text='Условия заказа и доставка 📦')
        ],
        [
            KeyboardButton(text='Заказать звонок 💌', request_contact=True),
            KeyboardButton(text='Оставить отзыв 💬')
        ],
    ],
    resize_keyboard=True
)


# Всплывающие кнопки для ссылок на соцсети
inline_kb_links = InlineKeyboardMarkup(row_width=2)
inline_kb_links.add(InlineKeyboardButton('Telegram', url=link_telegram))
inline_kb_links.add(InlineKeyboardButton('ВКонтакте', url=link_vk))
inline_kb_links.add(InlineKeyboardButton('Instagram', url=link_instagram))
inline_kb_links.add(InlineKeyboardButton('WhatsApp', url=link_whatsapp))


# Всплывающая кнопка для перехода на примеры работ
inline_kb_represent = InlineKeyboardMarkup(row_width=2)
inline_kb_represent.add(InlineKeyboardButton('🌸 Примеры работы в Instagram 🌸', url=link_instagram))
