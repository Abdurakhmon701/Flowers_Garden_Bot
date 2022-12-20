from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from api import get_category_id,category_get_all,get_product_by_category,get_basket_all_by_telegram_id
answer = ReplyKeyboardMarkup(
	keyboard = [
	[
	KeyboardButton(text = '🪴 Flowers Garden 🌳')
	],
	[
	KeyboardButton(text = '📞 Связь '),
	KeyboardButton(text = 'Корзина')
	],
	],
	resize_keyboard = True
)

	
 


async def for_category_get_all():
	x = category_get_all()
	categories = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		button_text = i["name"]
		callback_data = i["id"]
		categories.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"products_{callback_data}")
			)
	return categories


async def for_product_get_all(category_id: int):
	x = get_product_by_category(category_id)
	products = InlineKeyboardMarkup(row_width = 2)
	for i in x:
		# print(i)
		button_text = i["product_name"]
		callback_data = i["id"]
		products.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"mahsulot_{callback_data}")
			)
		products.insert(
			InlineKeyboardButton(text="Назад",callback_data=f"back_back1")
			)
	return products
	 

async def for_basket_all(telegram_id):
	data = get_basket_all_by_telegram_id(telegram_id)


	# data2 = delete_all_basket_products(telegram_id)
	# if data2 != []:
	#   for i in data:
	#     button_text = i["product_name"]
	#     callback_data = i["product_id"]
	#     price = i['product_price'].replace(' ','')
	#     products.insert(
	#       InlineKeyboardButton(text=f" {button_text}",callback_data=f"basket_{callback_data}")
	#       )
	#   return products


	products = InlineKeyboardMarkup(row_width = 2)
	products.add(
		InlineKeyboardButton(text='🔄 Очистить корзину',callback_data='delete_all'),
		InlineKeyboardButton(text='📝 Оформить заказ',callback_data=f'order_'))
	if data != []:
		for i in data:
			button_text = i["product_name"]
			callback_data = i["product_id"]
			price = i['product_price'].replace(' ','')
			products.add(
			InlineKeyboardButton(text=f"❌ {button_text}",callback_data=f"basket_{callback_data}")
			)
		return products

	return {'message':False}



# async def telephone_number_and_location():
#   number_and_location = InlineKeyboardMarkup()
#   number_and_location.insert(
#     InlineKeyboardButton(text="Номер телефона",callback_data=f"tel",request_contact=True)
#     )
	
#   return number_and_location

number = ReplyKeyboardMarkup(
	keyboard = [
	[
	KeyboardButton(text="Номер телефона:",request_contact=True)
	],
	[
	KeyboardButton(text="❌ Отменить процесс: ")
	],
	],
	resize_keyboard = True
	
)
location = ReplyKeyboardMarkup(
	keyboard = [
	[
	KeyboardButton(text="Локация:",request_location=True)
	],
	[
	KeyboardButton(text="❌ Отменить процесс: ")
	],
	],
	resize_keyboard = True
	
)
cancel = ReplyKeyboardMarkup(
	keyboard = [
	
	],
	resize_keyboard = True
	
)

agreeing = InlineKeyboardMarkup(row_width=1)
agreeing.add(
		InlineKeyboardButton(text="Да, продолжить",callback_data='agreeing')
		)


payment = InlineKeyboardMarkup(row_width=2)
payment.add(
		InlineKeyboardButton(text="Click",callback_data='payment_click'),
		InlineKeyboardButton(text='Payme',callback_data='payment_payme')
		)