import base64
from aiogram.filters import CommandStart, CommandObject

from keyboards.default.register import main_button
from loader import dp, db, bot
from aiogram import types
from states.all import RegisterState
from aiogram.fsm.context import FSMContext


# async def decode(id):
#     # Decoding the Base64 back to integer
#     decoded_num = int(base64.b64decode(id).decode())
#     return decoded_num


@dp.message(CommandStart())
async def start_chat(message: types.Message, state: FSMContext, command: CommandObject):
    user_id = message.from_user.id
    user = await db.select_user(user_id)

    if user:
        await message.answer("Bosh Menu", reply_markup=main_button())
    else:
        await register_new_user(message, command.args, user_id)
        await message.answer(
"Assalomu alaykum,Shohida Ibragimova tomondan tashkillashtirolayotgan Boylik Formulasi deb nomalangan Vebinarning yordamchi botiga xush kelibsiz! \n\n"
"<b>🤖Bu bot sizga qanday yordam bera oladi?</b> \n\nUshbu bot orqali siz Ekspert Shohida Ibragimova tomonidan tayyorlangan sovg’alarni qo’lga kiritish uchun shartlarni "
"bajarib sovg’alarni qo’lga kiritishingiz mumkin!\n\n"
"Ro'yxatdan o'tish Uchun Ism va Familiyangizni yuboring:"
"<b>Masalan: Karshiboev Ilyos</b>",
            parse_mode='HTML'
        )
        await state.set_state(RegisterState.full_name)


async def register_new_user(message, data, user_id):
    full_name = message.from_user.full_name
    username = message.from_user.username

    refer_id = await decode_data(data)
    if refer_id != 0:
        await db.add_user_with_competition_refer_id(
            full_name=full_name,
            telegram_id=user_id,
            username=username,
            competition_refer_id=refer_id
        )
    else:
        await db.add_user(
            full_name=full_name,
            telegram_id=user_id,
            username=username
        )


async def decode_data(data):
    try:
        return int(base64.b64decode(data).decode())
    except Exception as err:
        return 0
