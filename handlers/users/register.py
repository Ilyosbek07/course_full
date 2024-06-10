import re
import base64
from aiogram.fsm.context import FSMContext
from keyboards.default.register import number_button, agree_button, main_button
from states.all import RegisterState
from loader import dp, db, bot
from aiogram import types, F


async def encod_id(id):
    # Encoding the integer to Base64
    encoded = base64.b64encode(str(id).encode()).decode()
    return encoded


async def decode(id):
    # Decoding the Base64 back to integer
    decoded_num = int(base64.b64decode(id).decode())
    return decoded_num


@dp.message(F.text, RegisterState.full_name)
async def reg_name(message: types.Message, state: FSMContext):
    is_correct = message.text.split(' ')
    if message.text and len(is_correct) >= 2:
        await state.update_data({"self_introduction": message.text})
        await message.answer("📞Telefon raqamingizni quyidagi tugmani bosgan holda yuboring.\n\n"
                             "👨‍💻Biz sizni tasdiqlash uchun shu yuborgan raqamingizga bir martalik xavfsizlik kodi yuboramiz.",
                             reply_markup=number_button())
        await state.set_state(RegisterState.phone_number)
    else:
        await message.answer("Faqat Text Formatda Kamida 2ta so'z bilan yozing")


@dp.message(RegisterState.phone_number, F.text)
@dp.message(RegisterState.phone_number, F.contact)
async def reg_phone_number(message: types.Message, state: FSMContext):
    if message.text:
        await message.answer("Iltimos pastdagi tugma orqali raqamingizni yuboring")
    elif message.contact.phone_number and message.from_user.id == message.contact.user_id:
        await state.update_data({"phone": message.contact.phone_number})
        offerta = ""
        for offer in await db.select_all_offerta():
            offerta += f"{offer['link']}\n"
        await message.answer(f"{offerta}\n<b>⚠️Davom etish uchun Ommaviy oferta-shartnoma shartlari bilan tanishib chiqib, roziligingizni bildirishingiz lozim.</b>",
                             parse_mode="HTML",
                             reply_markup=agree_button())
        await state.set_state(RegisterState.is_agree)
    else:
        await message.answer("Iltimos pastdagi tugma orqali Shaxsiy raqamingizni yuboring")


@dp.message(RegisterState.is_agree, F.text)
async def reg_agree(message: types.Message, state: FSMContext):
    if message.text == "✅ Roziman":
        await message.answer("Karta Raqamingizni Yuboring")
        await state.set_state(RegisterState.card)
    else:
        await message.answer("Iltimos pastdagi '✅ Roziman' tugmasini bosing")


@dp.message(RegisterState.card, F.text)
async def reg_card(message: types.Message, state: FSMContext):
    pattern = r"^\d{16}$|^(\d{4}\s){3}\d{4}$"
    bot_link = await bot.get_me()
    encoded_user_id = await encod_id(message.from_user.id)

    if message.text and re.match(pattern, message.text):
        data = await state.get_data()
        await message.answer("<b>🎁 Sizga birinchi sovg’am!</b>\n\nHozirda biznesmi yoki qanday soha bo’lmasin "
                             "uning rivoji uchun <b>Ijtimoiy tarmoqlar</b> katta maydon bo’lib xizmat qilmoqda. "
                             "Har kuni ijtimoiy tarmoqlar orqali millionlab daromad qilayotgan SMM mutaxasislarni "
                             "eshitgan bo’lsangiz kerak. Xo’sh Instagram, Telegram, Meta va boshqa ijtimoy tarmoqlar"
                             " orqali qanday qilib masofadan pul ishlash mumkin? Bu zamonaviy sohani sir-asrorlari "
                             "nimadan iborat? \n\nBu savollarga javob topish maqsadida marketolog va SMM eksperti: "
                             "<b>Munisa Hakberdievaning “Smm va Marketing” </b>nomli 10 ta qisimdan iborat <b>video"
                             " darsligini "
                             "</b>sizga bepul taqdim qilmoqchiman!Ushbu darslikni qo’lga kiritish uchun "
                             "quyidagi postni o’qing⬇️⬇️⬇️",
                             parse_mode='HTML')
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
                             reply_markup=main_button())
        # await message.answer("Muvaffaqiyatli Ro'yxatdan o'tdingiz 🎊",
        #                      reply_markup=main_button())
        await db.update_user_data(
            full_name=data["self_introduction"],
            phone=data["phone"],
            card=f"{message.text.replace(' ', '')}",
            telegram_id=message.from_user.id
        )
        await state.clear()
    else:
        await message.answer("Iltimos karta raqamingizni to'g'ri yozing!(8600 1221 1255 1234)")
