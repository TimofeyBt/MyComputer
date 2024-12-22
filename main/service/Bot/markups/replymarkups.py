from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_reply = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Снимок экрана")],
        [KeyboardButton(text="Система 'Защитник'")],
        [KeyboardButton(text="Отправить сообщение")],
        [KeyboardButton(text="Заблокировать ПК")],
        [KeyboardButton(text="Выключить ПК"), KeyboardButton(text="Перезагрузить ПК")]
    ]
)