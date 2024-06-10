import os
import re
from loader import dp, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from keyboards.default.register import course_button, main_button
from states.all import SettingsState, Withdraw
from environs import Env

env = Env()
env.read_env()


class DepositCallback(CallbackData, prefix="ikb0002"):
    name: str


@dp.message(F.text == '💸 Hisobim')
async def deposit_user(message: types.Message, state: FSMContext):
    user = await db.select_user(message.from_user.id)
    inline_btn = InlineKeyboardBuilder()
    inline_btn.button(text="💸 Pul Yechib Olish", callback_data=DepositCallback(name="withdraw"))
    inline_btn.adjust(1)
    await message.answer(f"👤 Foydalanuvchi: {user['full_name']}\n"
                         f"💸 Hisob: {user['deposit']}\n",
                         reply_markup=inline_btn.as_markup())


@dp.callback_query(DepositCallback.filter())
async def withdraw_user(call: types.CallbackQuery, callback_data: DepositCallback, state: FSMContext):
    user = await db.select_user(call.from_user.id)
    await call.answer(cache_time=60)
    name = callback_data.name
    if name == "withdraw" and user['deposit'] > 30000:
        await call.message.answer("Qancha Pul Yechib Olmoqchisiz?")
        await state.set_state(Withdraw.withdraw)
    else:
        await call.message.answer("Hisobingizda yetarli mablag' mavjud emas")


@dp.message(F.text, Withdraw.withdraw)
async def withdraw_user(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        amount = int(message.text)
        user = await db.select_user(message.from_user.id)
        if user['deposit'] >= amount:
            # await db.update_user_deposit(telegram_id=message.from_user.id, deposit=amount, operation='withdraw')
            await message.answer("So'rov yuborildi")
            await state.clear()
        else:
            await message.answer(f"Hisobingizda yetarli mablag' mavjud emas\n\n"
                                 f"Hozirda Hisobingizda: {user['deposit']} so'm mavjud")
    else:
        await message.answer("Faqat son kiriting")
