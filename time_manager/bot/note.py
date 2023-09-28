from fastapi import HTTPException

from aiogram import types
from aiogram.utils import exceptions
from aiogram.utils.callback_data import CallbackData

from time_manager.bot import dp, bot
from time_manager.bot.note_handlers import get_note_fields
from time_manager.services.auth import AuthService
from time_manager.services.tg_user import TgUserService


ActionCallbackData = CallbackData('action', 'action')

main_keyboard = types.InlineKeyboardMarkup()
main_keyboard.add(
    types.InlineKeyboardButton(
        'Добавить время',
        callback_data=ActionCallbackData.new(action='add')
    ),
    types.InlineKeyboardMarkup(
        'Убрать время',
        callback_data=ActionCallbackData.new(action='sub')
    )
)


@dp.message_handler(commands="start")
async def start(
        message: types.Message,
):
    if len(message.text.split()) < 2:
        jwt_token = message.text.split()[1]
        try:
            user = AuthService.get_current_user(jwt_token)
        except HTTPException:
            await message.answer(text='Ошибка авторизации. Обратитесь в поддержку')
        else:
            with TgUserService() as tg_user_service:
                await tg_user_service.create(user.id, message.from_user.id)
            await message.answer(text='Выберите действие', reply_markup=main_keyboard)
    else:
        await message.answer(text='Ошибка авторизации. Обратитесь в поддержку')


@dp.callback_query_handler(ActionCallbackData.filter(action='add'))
async def add_hours(callbaack_query: types.CallbackQuery,
                    callback_data: dict):
    note = await get_note_fields(callbaack_query)
    print(note, note.states, note.states_names)
