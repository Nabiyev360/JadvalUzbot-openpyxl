from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.dbxl import add_data, get_dars, get_num_user
from keyboards.inline.addDarsInline import add_dars_inline
from keyboards.inline.editDarsInline import days_inline
from states.newSience import NewSience
from data.config import ADMINS

days_list = ["1️⃣ Dushanba", "2️⃣ Seshanba", "3️⃣ Chorshanba", "4️⃣ Payshanba", "5️⃣ Juma", "6️⃣ Shanba"]
days_dict = {"1️⃣ Dushanba":"D", "2️⃣ Seshanba":"F", "3️⃣ Chorshanba":"H", "4️⃣ Payshanba":"J", "5️⃣ Juma":"L", "6️⃣ Shanba":"N"}
days_dict2 = {"Dushanba":"D", "Seshanba":"F", "Chorshanba":"H", "Payshanba":"J", "Juma":"L", "Shanba":"N"}

@dp.message_handler(state=NewSience.sience_name)
async def new_siense(message: types.Message, state: FSMContext):
    data = await state.get_data()
    day_name = data.get(f"day_name{message.chat.id}")

    #User yuborgan darslar ro'yxatini bazaga qo'shish
    add_data(f'{days_dict2[day_name]}{get_num_user(message)}', message.text)
    
    await message.answer("Darslar ro'yxati muvaffaqiyatli qo'shildi✅", reply_markup = days_inline)
    await state.finish()         #state'dan chiqamiz ( & state datasi clear bo'ladi)
    await message.forward(ADMINS[0])

@dp.message_handler(text = '📝 Jadvalni o\'zgartirish')
async def edit_lesson(message: types.Message):
    await message.answer('Kiritmoqchi / O\'zgartirmochi bo\'lgan kuningizni tanlang', reply_markup=days_inline)

@dp.message_handler(text = '✍️ Izoh qoldirish')
async def send_lesson(message: types.Message):
    await message.answer('Bot haqida fikr, mulohaza va takliflaringiz bo\'lsa shu yergda yuboring💁‍♂')

@dp.message_handler()
async def send_dars(message: types.Message):
    if message.text=='getdb':
        file = open('db.xlsx', 'rb')
        await message.answer_document(file)
        file.close()
    
    elif message.text in days_list:
        darslar = get_dars(message, days_dict[message.text])
        # keyboard = buttons
        keyboard = None
        if "kiritilmagan" in darslar:
            keyboard = add_dars_inline
            
        await message.answer(darslar, reply_markup=keyboard)
        await message.forward(ADMINS[0])

@dp.message_handler(content_types=['photo', 'audio', 'video', 'document', 'voice', 'gif', 'sticker'])
async def for_others(message: types.Message):
    await message.forward(ADMINS[0])