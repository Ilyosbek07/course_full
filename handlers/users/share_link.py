import base64
from loader import dp, db, bot
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from environs import Env

env = Env()
env.read_env()


async def encod_id(id):
    # Encoding the integer to Base64
    encoded = base64.b64encode(str(id).encode()).decode()
    return encoded


async def decode(id):
    # Decoding the Base64 back to integer
    decoded_num = int(base64.b64decode(id).decode())
    return decoded_num


@dp.message(F.text == '♻️ Ulashish Posti')
async def share_course_link(message: types.Message, state: FSMContext):
    bot_link = await bot.get_me()
    encoded_user_id = await encod_id(message.from_user.id)
    # await message.answer(f"Sizga ajoyib kursni taklif qilaman."
    #                      f"Kursni olish uchun havola 👇\n\n"
    #                      f"https://t.me/{bot_link.username}?start={encoded_user_id}")
    await message.answer(f"✅Sovg’alarimni olish uchun sizdan birgina harakat kerak!\n\n "
                         f"Moliyaviy savodxonlik bo’yicha O’zbekistondagi №1 ekspert Shohida"
                         f" Ibragimovavning (t.me/shohida_ibragimova) kanaliga sizga beriladigan "
                         f"<b>“Referal”</b> havolani va shu botni orqali 10 ta yaqinlaringiznga yuboring!"
                         f"\n\n<b>Referal havolalar ⬇️⬇️⬇️\n\n"
                         f"1- qadam: <a href='https://t.me/{bot_link.username}?start={encoded_user_id}'>Moliyaviy Parhez</a> ga kirib ro’yxatdan"
                         f" o’tish\n\n"
                         f"2- qadam: <a href='https://t.me/shohida_ibragimova'>Mahsus Link</a> orqali kirib kanalga qo’shilish\n\n"
                         f"⬆️⬆️⬆️</b> "
                         f"\n\n“Tekshirish” tugmasi orqali siz orqali nechta odam kanalga obuna bo’lganini "
                         f"tekshshiringiz mumkin, obunalar soni 10 taga yetganda yopiq guruh linki avtomatik "
                         f"bot orqali sizga yuboriladi, guruhga allaqachon videodarslar yuklangan!"
                         f" \n\n<b>Ilm olish va ulashishdan charchamang!</b>",
                         parse_mode='HTML',
                         )
    await message.answer("👆 Yuqorida Kursni ulashish uchun sizning shaxsiy havolangiz."
                         "Uni do'stlaringiz bilan ulashing va bo'nus darsga ega bo'ling.\n\n"
                         "10ta do'stingiz kanalga A'zo bo'lsa siz Yopiq kanalga link olasiz")
