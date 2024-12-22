import threading

import aiogram
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from service import pc_management
from service.Bot.markups import inlinemarkups, replymarkups
from service.Bot import forms

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Приветствую, владелец!", reply_markup=replymarkups.main_reply)


@router.message(lambda msg: msg.text == "Система 'Защитник'")
async def system_safer_handler(message: Message):
    safer_status = pc_management.get_safer_status()
    await message.answer(f"Статус системы 'Защитник' - <b>{"Включена" if safer_status else "Выключена"}</b>",
                         parse_mode="HTML",
                         reply_markup=inlinemarkups.safer_off_markup if safer_status else inlinemarkups.safer_on_markup)


@router.callback_query(lambda callback: callback.data == "system_safer_on")
async def system_safer_on_handler(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    if not pc_management.get_safer_status():
        threading.Thread(target=pc_management.start_system_safer).start()
        await callback.message.answer("Система 'Защитник' успешно <b>Включена</b>",
                                      parse_mode="HTML",
                                      reply_markup=replymarkups.main_reply)
    else:
        await callback.message.answer("Система 'Защитник' уже была <b>включена</b>",
                                      parse_mode="HTML",
                                      reply_markup=replymarkups.main_reply)


@router.callback_query(lambda callback: callback.data == "system_safer_off")
async def system_safer_off_handler(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    if pc_management.get_safer_status():
        pc_management.stop_system_safer()
        await callback.answer("Система 'Защитник' успешно <b>Выключена</b>",
                              parse_mode="HTML",
                              reply_markup=replymarkups.main_reply)
    else:
        await callback.answer("Система 'Защитник' уже была <b>выключена</b>",
                              parse_mode="HTML",
                              reply_markup=replymarkups.main_reply
                              )


@router.message(lambda msg: msg.text == "Снимок экрана")
async def screenshot_handler(message: Message):
    await message.answer_photo(BufferedInputFile(file=pc_management.get_screenshot(), filename="Screenshot.png"))


@router.message(lambda msg: msg.text == "Заблокировать ПК")
async def PClock_handler(message: Message):
    pc_management.lock()
    await message.answer("ПК успешно <b>Заблокирован</b>",
                         parse_mode="HTML",
                         reply_markup=replymarkups.main_reply)


@router.message(lambda msg: msg.text == "Выключить ПК")
async def off_pc_handler_fromReply(message: Message):
    await message.answer("<b>Выключаю</b> ваш ПК",
                         parse_mode="HTML",
                         reply_markup=replymarkups.main_reply)
    pc_management.off()


@router.callback_query(lambda callback: callback.data == "off_pc")
async def off_pc_handler_fromInline(callback: CallbackQuery):
    await callback.message.answer("<b>Выключаю</b> ваш ПК",
                                  parse_mode="HTML",
                                  reply_markup=replymarkups.main_reply)
    pc_management.off()


@router.message(lambda msg: msg.text == "Перезагрузить ПК")
async def restart_pc_handler(message: Message):
    await message.answer("<b>Перезагружаю</b> ваш ПК",
                         parse_mode="HTML",
                         reply_markup=replymarkups.main_reply)
    pc_management.restart()


@router.message(lambda msg: msg.text == "Отправить сообщение")
async def send_notification_handler(message: Message, state: FSMContext):
    await message.answer("Введите текст сообщения")

    await state.set_state(forms.SendNotification.waiting_text)


@router.message(forms.SendNotification.waiting_text, aiogram.F.text)
async def send_notification_text_handler(message: Message, state: FSMContext):
    threading.Thread(target=pc_management.send_notification, args=(message.text,)).start()

    await message.answer(f"<b>Сообщение:</b>\n'<i>{message.text}</i>'\nуспешно отправлено",
                         parse_mode="HTML",
                         reply_markup=replymarkups.main_reply)

    await state.clear()
