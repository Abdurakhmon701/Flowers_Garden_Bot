from aiogram import types
from keyboards.inline.category_keyboard import *
from loader import dp



# Pastki knopka flowers garden
@dp.message_handler(text = "🪴 Flowers Garden 🌳",state="*")
async def echo(message: types.Message):
	buttons = await for_category_get_all()
	await message.answer('categories',reply_markup = buttons)




@dp.message_handler(text = "Корзина")
async def echo(message: types.Message):
	buttons = await for_card(message.from_user.id)
	await message.answer("TEST",reply_markup=buttons)
