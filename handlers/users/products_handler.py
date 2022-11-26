from aiogram import types
from keyboards.inline.category_keyboard import *
from aiogram.utils.callback_data import CallbackData
from loader import dp,bot
from aiogram.dispatcher.filters import Text
from api import *
from states.all_data import *
from aiogram.dispatcher import FSMContext

user_data = {}


callback_numbers = CallbackData("fabnum","id", "action",)


def get_keyboard_fab(new_value:int,idi):
	buttons = [
		types.InlineKeyboardButton(text="-", callback_data=callback_numbers.new(id=idi,action="decr")),
		types.InlineKeyboardButton(text=f"{new_value}", callback_data="num_result"),
		types.InlineKeyboardButton(text="+", callback_data=callback_numbers.new(id=idi,action="incr")),
		types.InlineKeyboardButton(text="Savatga kiritish", callback_data=callback_numbers.new(id=idi,action="finish"))
	]

	keyboard = types.InlineKeyboardMarkup(row_width=3)
	keyboard.add(*buttons)
	# data = get_product_id(idi)
	# print(data['category'])
	# keyboard.insert(
	# 		types.InlineKeyboardButton(text = 'Назад',callback_data = f"pro_{data['category']}"))
	return keyboard

# Pastki knopka flowers garden
@dp.callback_query_handler(Text(startswith='products_'),state='*')
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	data = await for_product_get_all(category_id)	
	await call.message.answer('mahsulotlar',reply_markup=data)
	await BuyurtmaData.score.set()

@dp.callback_query_handler(Text(startswith='back_'),state='*')
async def echo(call: types.CallbackQuery):
	all_data = call.data.index('_')
	category_id = call.data[all_data+1:]
	print(call.data)
	buttons = await for_category_get_all()
	await call.message.answer('categories',reply_markup = buttons)
	
	


@dp.callback_query_handler(Text(startswith='mahsulot_'),state=BuyurtmaData.score)
async def echo(call: types.CallbackQuery,state: FSMContext):
	all_data = call.data.index('_')
	url = 'http://127.0.0.1:8000/media'
	category_id = call.data[all_data+1:]
	data = get_product_id(category_id)
	print(call.data)
	user_data[call.from_user.id] = 1
	await bot.send_photo(call.from_user.id,caption=f"{data['product_name']}\n\n{data['product_description']},\n💰 {data['product_price']} сум",photo="https://rastenievod.com/wp-content/uploads/2016/06/1-84-700x705.jpg",reply_markup=get_keyboard_fab(1,data['id']))
	await state.finish()


@dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]),)
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict,state: FSMContext):
	user_value = user_data.get(call.from_user.id, 1)
	action = callback_data["action"]
	# await state.update_data({"user_id": call.from_user.id}) 
	post_id = callback_data["id"]
	# data1 = db.select_category_id(post_id)
	# print(data1)
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


@dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery,callback_data: dict):
	post_id = callback_data["id"]
	data1 = get_product_id(post_id)
	user_value = user_data.get(call.from_user.id, 0)
	post_card(call.from_user.id,data1['id'],data1["product_name"],data1['product_price'])
	# await call.message.answer(f"Savatga kirilidi:\n\nMahsulot nomi: {data1['product_name']} \nID: {data1['id']} \nMahsulot narxi: {data1['product_price']}\nSoni: {user_value}")
	await call.answer("Добавлено")
	buttons = await for_category_get_all()
	await call.message.answer('categories',reply_markup = buttons)


# @dp.callback_query_handler(Text(startswith='pro_'),state='*')
# async def echo(call: types.CallbackQuery):
# 	all_data = call.data.index('_')
# 	category_id = call.data[all_data+1:]
# 	print(category_id)
# 	data = await for_product_get_all(category_id)	
# 	await call.message.answer('mahsulotlar',reply_markup=data)
# 	await BuyurtmaData.score.set()


	# products = types.InlineKeyboardMarkup(row_width = 3)
	# for i in range(10,101,10):
	# 	products.insert(
	# 		types.InlineKeyboardButton(text = i,callback_data = 'i'))

	# products.insert(
	# 		types.InlineKeyboardButton(text = 'Платёж',callback_data = 'back_Pro'))
	# products.insert(
	# 		types.InlineKeyboardButton(text = 'Назад',callback_data = f"products_{data['category']}"))
	# await bot.send_photo(call.from_user.id,caption=f"{data['product_name']}\n\n{data['product_description']},\n💰 {data['product_price']} сум",photo="https://rastenievod.com/wp-content/uploads/2016/06/1-84-700x705.jpg",reply_markup=products)