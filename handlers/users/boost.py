import base64
from loader import dp, db, bot
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from environs import Env
from typing import Union

from aiogram import Bot

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


async def check(user_id, channel: Union[int, str]):
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.status == 'member'


@dp.message(F.text == 'Tekshirish')
async def check_count(message: types.Message):
    counter = 0
    refer_users = await db.select_all_competition_refer_id(message.from_user.id)
    for refer_user in refer_users:
        status = await check(user_id=refer_user['telegram_id'], channel="@shohida_ibragimova")
        if status:
            counter += 1
    await message.answer(f"🔥 Sizning {counter} ta do'stingiz kanalga obuna bo'lgan.")
    if counter == 10:
        try:
            ChatInviteLink = await bot.create_chat_invite_link(member_limit=1, chat_id='-1002201206839')
            await message.answer(f"🔥 Sizning taklif havolangiz:\n\n{ChatInviteLink.invite_link}")
        except Exception as err:
            ChatInviteLink = await bot.create_chat_invite_link(member_limit=1, chat_id='-1002201206839')
            await message.answer(f"🔥 Sizning taklif havolangiz:\n\n{ChatInviteLink.invite_link}")


@dp.message(F.text == '🔥 Boost 2X')
async def share_course_link(message: types.Message, state: FSMContext):
    bot_link = await bot.get_me()
    encoded_user_id = await encod_id(message.from_user.id)
    await message.answer(f"Sizga ajoyib kursni taklif qilaman."
                         f"Kursni olish uchun havola 👇\n\n"
                         f"https://t.me/{bot_link.username}?start={encoded_user_id}")
    await message.answer("👆 Yuqorida Kursni ulashish uchun sizning shaxsiy havolangiz."
                         "Agarda Kursni sotib olgan bo'lsangiz sizning linkingiz orqali kirgan har bitta odam uchun"
                         " 80.000 so'mni qo'lga kiritasiz.")
