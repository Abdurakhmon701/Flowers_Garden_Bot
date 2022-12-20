from aiogram import types
from loader import dp,bot
from keyboards.inline.category_keyboard import *
from aiogram.dispatcher.filters import Text
from api import *
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext
from states.all_data import BuyurtmaData,OrderInfoData

from utils.misc.product import Product
from aiogram.types import LabeledPrice

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import *

user_data = {}


callback_numbers = CallbackData("fabnum","id", "action",)


def get_keyboard_fab(new_value:int,idi,state="*"):
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.add(
				types.InlineKeyboardButton(text="-", callback_data=callback_numbers.new(id=idi,action="decr")),
				types.InlineKeyboardButton(text=f"{new_value}", callback_data="num_result"),
				types.InlineKeyboardButton(text="+", callback_data=callback_numbers.new(id=idi,action="incr")),
				types.InlineKeyboardButton(text="Добавить в корзину", callback_data=callback_numbers.new(id=idi,action="finish"))
			)

	
	keyboard.add(types.InlineKeyboardButton(text="Назад",callback_data=f"products_{idi}"))
	return keyboard



@dp.callback_query_handler(Text(startswith='products_'),state='*')
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	buttons_for_products = await for_product_get_all(category_id)
	await call.message.answer('<b>Выберите количество продуктов, затем добавьте в корзину: </b>',reply_markup=buttons_for_products)
	await BuyurtmaData.score.set()

@dp.callback_query_handler(Text(startswith='back_'),state="*")
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	buttons_for_category = await for_category_get_all()
	await call.message.answer('<b>Выберите категорию : </b>',reply_markup=buttons_for_category)
	

@dp.callback_query_handler(Text(startswith='mahsulot_'),state=BuyurtmaData.score)
async def echo(call: types.CallbackQuery,state: FSMContext):
	all_data = call.data.index('_')
	url_for_photo = "http://127.0.0.1:8000/media"
	category_id = call.data[all_data+1:]
	data = get_product_id(category_id)
	user_data[call.from_user.id] = 1
	await bot.send_photo(call.from_user.id,caption = f"{data['product_name']}\n\n{data['product_description']},\n{data['product_price']} сум",photo="https://sdelai-lestnicu.ru/wp-content/uploads/7/5/8/758b960e7ae8f2c173de5688a83b3461.jpg",reply_markup=get_keyboard_fab(1,data['id']))
	await state.finish()
@dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]),)
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict,state: FSMContext):
	user_value = user_data.get(call.from_user.id, 1)
	action = callback_data["action"]
	post_id = callback_data["id"]
	data = await state.get_data()
	tel_ = data.get("tel_")
	if action == "incr":
		user_data[call.from_user.id] = user_value + 1
		# await update_num_text_fab(call.message, user_value + 1)
		await call.message.edit_reply_markup(reply_markup=get_keyboard_fab(user_value+1,post_id))
		await call.answer(f"{user_value+1} шт.")
		await state.reset_state()
	elif action == "decr":
		if user_value != 1:
			user_data[call.from_user.id] = user_value - 1
			await call.message.edit_reply_markup(reply_markup=get_keyboard_fab(user_value-1,post_id))
			await call.answer(f"{user_value-1} шт.")
			await state.reset_state()

	await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["finish"]),state="*")
async def callbacks_num_finish_fab(call: types.CallbackQuery,callback_data: dict):
	post_id = callback_data["id"]
	data1 = get_product_id(post_id)
	user_value = user_data.get(call.from_user.id, 0)
	basket = get_for_basket(call.from_user.id,data1['id'])
	print(basket)
	if basket:
		count_basket(call.from_user.id,data1['id'],user_value)
		await call.message.answer("<b> Продукт обновлён !</b>")     
	else:
		post_for_basket(call.from_user.id,data1['id'],data1['product_name'],data1['product_price'],user_value)
		await call.answer("<b>Добавлено</b>")
		buttons_for_category = await for_category_get_all()
		await call.message.answer('<b>Выберите категорию : </b>',reply_markup=buttons_for_category)
	


@dp.callback_query_handler(Text(startswith='basket_'),state="*")
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	delete_for_basket(call.from_user.id,category_id)
	buttons_for_basket = await for_basket_all(call.from_user.id)
	if 'message' in buttons_for_basket:
		await call.message.edit_text("<b> Ваша корзина пусто </b>")
	else:
		await call.message.edit_reply_markup(reply_markup=buttons_for_basket)


@dp.callback_query_handler(text='delete_all',state="*")
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	delete_all_basket_products(call.from_user.id)
	buttons_for_category = await for_category_get_all()
	await call.message.answer("<b> Ваша корзина успешно удалена!</b>",reply_markup=buttons_for_category)
	buttons_for_basket = await for_basket_all(call.from_user.id)
	if 'message' in buttons_for_basket:
		await call.message.edit_text("<b> Ваша корзина пусто </b>")
	else:
		await call.message.edit_reply_markup("""<b> «❌ Наименование - удалить одну позицию»
«🔄 Очистить - полная очистка корзины»</b>""",reply_markup=buttons_for_basket)

 
@dp.message_handler(text = "❌ Отменить процесс:",state="*")
async def echo(message: types.Message):
	delete_all_basket_products(message.from_user.id)
	await message.answer('<b>Процесс отменён </b>',reply_markup=answer)



@dp.message_handler(text = "📞 Связь ",state="*")
async def echo(message: types.Message):
	await message.answer(f'Test{ADMINS[0]}')



@dp.callback_query_handler(text='order_',state="*")
async def echo(call: types.CallbackQuery,state: FSMContext):
	await call.message.answer("""<b>❗️ Уважаемый клиент, пожалуйста, прочитайте внимательно!

Наш магазин Flowers Garden обслуживает только города Ташкента и Ташкентскую области!
Оплата доступна только в системе Click !

За неправильный адрес и оплату 
ответственность нести будете вы !
Пожалуйста, пришлите правильный адрес !</b>""",reply_markup=agreeing)
	
	
@dp.callback_query_handler(text='agreeing',state=None)
async def echo(call: types.CallbackQuery,state: FSMContext):
	await call.message.answer("""<b>Отправьте номер телефона: </b>""",reply_markup=number)
	await OrderInfoData.raqam.set()



@dp.message_handler(content_types = ["contact"],state=OrderInfoData.raqam)
async def echo(message: types.Message,state: FSMContext):
	contact = message.contact['phone_number']
	print(contact)
	await state.update_data({"contact":contact})  
	await message.answer("<b>Отправьте местоположение: </b>",reply_markup = location)

	await OrderInfoData.location.set()


@dp.message_handler(content_types = ["location"],state=OrderInfoData.location)
async def echo1(message: types.Message,state: FSMContext):
	data = await state.get_data()
	location_y = message.location["longitude"]
	location_x = message.location['latitude']
	await state.update_data({"address":{"location_x":location_x,"location_y":location_y}})
	await message.answer('<b>Выберите способ оплаты: </b>',reply_markup=payment)
	await OrderInfoData.payment.set()

@dp.callback_query_handler(Text(startswith='payment_'),state=OrderInfoData.payment)
async def echo(call: types.CallbackQuery,state: FSMContext):
	all_data = call.data.index('_')
	pay = call.data[all_data+1:]
	print(pay)
	await call.message.answer("<b> Минуточку.. </b>")
	information = get_basket_all_by_telegram_id(call.from_user.id)
	products_list = ''
	all_sum = 0
	if pay=="click":
		await state.update_data({"tulov":"click"})
		for info in  information:
			products_list+= f"\n{info['product_name']}\n"
			product_price = info['product_price']
			new_product_price = product_price.replace(' ',"")
			# print(f"{info['product_name']}*{info['count']}={int(new_product_price)*int(info['count'])},{info['product_price']}")
			all_sum += int(new_product_price)*int(info['count']) 

		product = Product(
			title="TestName",
			description="TestDescription",
			currency="UZS",
			prices=[
				LabeledPrice(
					label = f"{info['product_name']}",
					amount=all_sum*100,
					),
				LabeledPrice(
					label="Доставка",
					amount=5000000,
					),
				],
			start_parameter="create_invoice_python_book",

			# need_name=True,
			# need_shipping_address=True,
			# need_phone_number=True,
			# is_flexible = False,
			provider_token = PROVIDER_TOKEN_CLICK
			)
		await bot.send_invoice(chat_id=call.from_user.id,**product.generate_invoice(),payload=f"{products_list}")
		await OrderInfoData.user_id.set()
	if pay == "payme":
		await state.update_data({"tulov":"payme"})
		for info in  information:
			products_list+= f"\n{info['product_name']}\n"
			product_price = info['product_price']
			new_product_price = product_price.replace(' ',"")
			# print(f"{info['product_name']}*{info['count']}={int(new_product_price)*int(info['count'])},{info['product_price']}")
			all_sum += int(new_product_price)*int(info['count']) 

		product = Product(
			title="TestName",
			description="TestDescription",
			currency="UZS",
			prices=[
				LabeledPrice(
					label = f"{info['product_name']}",
					amount=all_sum*100,
					),
				LabeledPrice(
					label="Доставка",
					amount=5000000,
					),
				],
			start_parameter="create_invoice_python_book",
			# need_name=True,
			# need_shipping_address=True,
			# need_phone_number=True,
			# is_flexible = False,
			provider_token = PROVIDER_TOKEN_PAYME
			)
		await bot.send_invoice(chat_id=call.from_user.id,**product.generate_invoice(),payload=f"{products_list}")
		await OrderInfoData.user_id.set()


USUSAL_SHIPPING = types.ShippingOption(
	id='post_usual',
	title = 'Fargo (3 kun)',
	prices = [
		LabeledPrice(
			'Maxsus quti',500000 
		),
		LabeledPrice(
			'3 kun ichida yetkazish',300000 
		),
	]
)

@dp.pre_checkout_query_handler(state=OrderInfoData.user_id)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery,state: FSMContext):
	delete_all_basket_products(pre_checkout_query.from_user.id)
	await bot.answer_pre_checkout_query(pre_checkout_query_id =pre_checkout_query.id,ok=True)
	
	
	await bot.send_message(chat_id=pre_checkout_query.from_user.id,text="<b>Спасибо за покупку и доверие!</b>",reply_markup=answer)
	data = await state.get_data()
	contact1 = data.get('contact')
	address1 = data.get('address')
	payment = data.get('tulov')
   
	post_for_order(
		f"{address1}",
		contact1,
		payment,
		pre_checkout_query.id,
		pre_checkout_query.invoice_payload,
		pre_checkout_query.total_amount,
		pre_checkout_query.order_info.name,
		pre_checkout_query.from_user.id,
		pre_checkout_query.from_user.username,
		pre_checkout_query.order_info.phone_number,
		)

	await state.finish()
	await bot.send_message(chat_id=ADMINS[0],
							text=f"Имя товара:\n{pre_checkout_query.invoice_payload}\n"
								f"ID:{pre_checkout_query.id}\n"
								f"Общая цена: {pre_checkout_query.total_amount}\n"
								f"Telegram Username:{pre_checkout_query.from_user.username}"
								)