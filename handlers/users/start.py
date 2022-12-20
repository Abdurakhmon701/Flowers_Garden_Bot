from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.category_keyboard import answer
from loader import dp

from api import user_scaning,post_for_user

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if user_scaning(message.from_user.id):
        await message.answer(f"""<b>Приветствуем вас в Flowers Garden!\n
Главное меню ⏬: </b>""",reply_markup=answer)
    else:
        post_for_user(message.from_user.id,message.from_user.username)
        await message.answer(f"""<b>Здравствуйте уважаемый клиент {message.from_user.full_name}, к вашим услугам Flowers Garden !
Главное меню ⏬ </b>""",reply_markup=answer)