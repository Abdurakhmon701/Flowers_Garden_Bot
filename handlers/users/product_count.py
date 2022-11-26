from states.all_data import *
@dp.message_handler(commands=['start', 'help'],state='*')
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.",reply_markup=get_keyboard1())
    await BuyurtmaData.score.set()



def get_keyboard1():
    # Генерация клавиатуры.
    data = db.select_category()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # print(data)
    for i in data:
        buttons = [
            types.InlineKeyboardButton(text=i[1], callback_data=f"product_{i[0]}/{i[2]}"),
        ]
        keyboard.add(*buttons)

    return keyboard

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
    return keyboard


@dp.callback_query_handler(Text(startswith="product_"),state=BuyurtmaData.score)
async def cmd_numbers(call: types.CallbackQuery,state: FSMContext):
    t = call.data.index('_')
    m = call.data.index('/')
    data = db.select_category_id(call.data[t+1:m])
    print(data)
    await state.update_data({"tel_": data}) 
    user_data[call.from_user.id] = 1
    await call.message.answer(f"Mahsulot nomi: {data[1]}\n\nNarxi: {data[2]}", reply_markup=get_keyboard_fab(1,data[0]))
    # await BuyurtmaData.next()
    await state.finish()
    


@dp.callback_query_handler(callback_numbers.filter(action=["incr", "decr"]),)
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict,state: FSMContext):
    user_value = user_data.get(call.from_user.id, 1)
    action = callback_data["action"]
    # await state.update_data({"user_id": call.from_user.id}) 
    post_id = callback_data["id"]
    data = await state.get_data()
    tel_ = data.get("tel_")
    data1 = db.select_category_id(post_id)
    print(data1)
    if action == "incr":
        user_data[call.from_user.id] = user_value + 1
        # await update_num_text_fab(call.message, user_value + 1)
        await call.message.edit_text(f"Mahsulot nomi: {(user_value + 1) * int(data1[2])}", reply_markup=get_keyboard_fab(user_value+1,post_id))
        await state.reset_state()
    elif action == "decr":
        if user_value != 1:
            user_data[call.from_user.id] = user_value - 1
            await call.message.edit_text(f"Mahsulot nomi: {(user_value - 1) * int(data1[2])}", reply_markup=get_keyboard_fab(user_value-1,post_id))
            await state.reset_state()

    await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery,callback_data: dict):
    post_id = callback_data["id"]
    data1 = db.select_category_id(post_id)
    print(data1)
    user_value = user_data.get(call.from_user.id, 0)
    await call.message.edit_text(f"Savatga kirilidi:\nMahsulot nomi: {data1[1]}\nSoni: {user_value}")
    await call.answer()

