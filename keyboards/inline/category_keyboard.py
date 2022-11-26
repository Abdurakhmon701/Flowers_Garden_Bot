from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from api import *
#================================================================================================================

# # Bu pastki menu uchun Rus
answer_start = ReplyKeyboardMarkup(
	keyboard = [
	[
		KeyboardButton(text = '🪴 Flowers Garden 🌳')
	],
	[
		KeyboardButton(text = '📞 Связь'),
		KeyboardButton(text = '⚙️ Настройки ')
	],
	[
		KeyboardButton(text = 'Корзина'),
	]
	],
	resize_keyboard = True
)

order = InlineKeyboardMarkup(
	keyboard = [
	[
		InlineKeyboardButton(text = '-'),
		InlineKeyboardButton(text = '1'),
		InlineKeyboardButton(text = '+'),
	],
	[
		InlineKeyboardButton(text = '100'),
	],
	],
	resize_keyboard = True
)

# async def for_category(idi):
# 	x = get_category_id(idi)
# 	for i in x:
# 		print(i)
		

		
async def for_category_get_all():
	x = category_get_all()
	categories = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		button_text = i['name']
		callback_data = i['id']
		categories.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"products_{callback_data}")
				)
	
	return categories



async def for_product_get_all(category_id: int):
	x = get_product_by_category(category_id)
	products = InlineKeyboardMarkup(row_width = 2)

	for i in x:
		# print(i)
		button_text = i['product_name']
		callback_data = i['id']
		products.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"mahsulot_{callback_data}")
				)
	products.insert(
			InlineKeyboardButton(text = 'Назад',callback_data = 'back_back1'))
	return products


async def for_card(telegram_id):
	data = get_card_all_by_id(telegram_id)
	# products1 = InlineKeyboardMarkup(row_width = 2)
	products = InlineKeyboardMarkup(row_width = 1)
	products.add(
		InlineKeyboardButton(text="nim",callback_data='n'))
	for i in data:
		# print(i)
		button_text = i['product_name']
		callback_data = i['id']
		products.insert(
			InlineKeyboardButton(text=f"❌ {button_text}",callback_data=f"card_{callback_data}")
				)
	return products


# KNopka qilish
# Demosni yozish uyda