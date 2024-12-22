from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

pc_start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Выключить ПК", callback_data="off_pc")
        ],
        [
            InlineKeyboardButton(text="Включить систему 'Защитик'", callback_data="system_safer_on")
        ]
    ]
)

safer_on_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Включить систему 'Защитик'", callback_data="system_safer_on")
        ]
    ]
)

safer_off_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Выключить систему 'Защитик'", callback_data="system_safer_off")
        ]
    ]
)
