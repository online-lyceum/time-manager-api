from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from time_manager.bot import dp, bot


class NoteForm(StatesGroup):
    minutes = State()
    text = State()


async def get_note_fields(message: types.Message):
    await message.answer('Введите минуты')
    await NoteForm.minutes.set()
    await message.answer('Введите текст(. для пустого сообщения)')
    await NoteForm.text.set()
    return NoteForm


@dp.message_handler(state=NoteForm.a)
async def _get_note_minutes(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        a['minutes'] = message.text
        await state.finish()


@dp.message_handler(state=NoteForm.a)
async def _get_note_text(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        a['text'] = message.text
        await state.finish()