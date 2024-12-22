from aiogram.fsm.state import StatesGroup, State


class SendNotification(StatesGroup):
    waiting_text = State()