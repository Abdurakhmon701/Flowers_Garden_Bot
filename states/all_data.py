from aiogram.dispatcher.filters.state import StatesGroup, State

class BuyurtmaData(StatesGroup):
	score = State()
	raqam = State()

class OrderInfoData(StatesGroup):
	raqam = State()
	location = State()
	payment = State()
	user_id = State()