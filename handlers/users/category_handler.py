from aiogram import types
from loader import dp
from keyboards.inline.category_keyboard import *



@dp.message_handler(text = "🪴 Flowers Garden 🌳",state="*")
async def echo(message: types.Message):
    buttons_for_category = await for_category_get_all()
    await message.answer('<b>Выберите категорию : </b>',reply_markup=buttons_for_category)



@dp.message_handler(text = "Корзина",state="*")
async def echo(message: types.Message):
    buttons_for_basket = await for_basket_all(message.from_user.id)
    if 'message' in buttons_for_basket:
        await message.answer("<b> Ваша корзина пусто </b>")
    else:
        await message.answer("""<b> «❌ Наименование - удалить один продукт из вашей корзины»\n\n
«🔄 Очистить корзину - полная очистка корзины»</b>""",reply_markup=buttons_for_basket)