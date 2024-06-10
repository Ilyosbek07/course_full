import os
import re
from loader import dp, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from keyboards.default.register import course_button, main_button
from states.all import SettingsState
from environs import Env

env = Env()
env.read_env()


class SettingsCallback(CallbackData, prefix="ikb0000"):
    name: str


@dp.message(F.text == '⚙️ Sozlamalar')
async def user_info(message: types.Message, state: FSMContext):
    user = await db.select_user(message.from_user.id)
    inline_btn = InlineKeyboardBuilder()
    inline_btn.button(text="👤 Ismni O'zgartirish", callback_data=SettingsCallback(name="change_user_name"))
    inline_btn.button(text="💳 Kartani O'zgartirish", callback_data=SettingsCallback(name="change_user_card"))
    inline_btn.button(text="📞 Telefon Raqamni O'zgartirish", callback_data=SettingsCallback(name="change_user_phone"))
    inline_btn.adjust(1)
    await message.answer(f"👤 Foydalanuvchi: {user['full_name']}\n"
                         f"📞 Telefon: {user['phone']}\n"
                         f"💳 Karta: {user['card']}\n",
                         reply_markup=inline_btn.as_markup())


@dp.callback_query(SettingsCallback.filter())
async def change_user_phone(call: types.CallbackQuery, callback_data: SettingsCallback, state: FSMContext):
    await call.answer(cache_time=60)
    name = callback_data.name
    if name == "change_user_phone":
        await call.message.answer("Yangi Telefon Raqamni kiriting")
        await state.set_state(SettingsState.phone)
    elif name == "change_user_card":
        await call.message.answer("Yangi Kartani kiriting")
        await state.set_state(SettingsState.card)
    elif name == "change_user_name":
        await call.message.answer("Yangi Ismingizni kiriting")
        await state.set_state(SettingsState.full_name)

@dp.message(F.text, SettingsState.phone)
async def change_user_phone(message: types.Message, state: FSMContext):
    phone_regex = re.compile(r'^\+998\d{9,12}$')
    if phone_regex.match(message.text):
        await db.update_user_phone(telegram_id=message.from_user.id, phone=message.text)
        await message.answer("Telefon Raqam O'zgartirildi")
        user = await db.select_user(message.from_user.id)
        inline_btn = InlineKeyboardBuilder()
        inline_btn.button(text="👤 Ismni O'zgartirish", callback_data=SettingsCallback(name="change_user_name"))
        inline_btn.button(text="💳 Kartani O'zgartirish", callback_data=SettingsCallback(name="change_user_card"))
        inline_btn.button(text="📞 Telefon Raqamni O'zgartirish",
                          callback_data=SettingsCallback(name="change_user_phone"))
        inline_btn.adjust(1)
        await message.answer(f"👤 Foydalanuvchi: {user['full_name']}\n"
                             f"📞 Telefon: {user['phone']}\n"
                             f"💳 Karta: {user['card']}\n",
                             reply_markup=inline_btn.as_markup())

        await state.clear()
    else:
        await message.answer("Telefon Raqamni To'g'ri Kiriting.(+998901234567)")


@dp.message(F.text, SettingsState.card)
async def change_user_card(message: types.Message, state: FSMContext):
    pattern = r"^\d{16}$|^(\d{4}\s){3}\d{4}$"
    if message.text and re.match(pattern, message.text):
        await db.update_user_card(telegram_id=message.from_user.id, card=message.text)
        await message.answer("Karta Raqam O'zgartirildi")
        user = await db.select_user(message.from_user.id)
        inline_btn = InlineKeyboardBuilder()
        inline_btn.button(text="👤 Ismni O'zgartirish", callback_data=SettingsCallback(name="change_user_name"))
        inline_btn.button(text="💳 Kartani O'zgartirish", callback_data=SettingsCallback(name="change_user_card"))
        inline_btn.button(text="📞 Telefon Raqamni O'zgartirish",
                          callback_data=SettingsCallback(name="change_user_phone"))
        inline_btn.adjust(1)
        await message.answer(f"👤 Foydalanuvchi: {user['full_name']}\n"
                             f"📞 Telefon: {user['phone']}\n"
                             f"💳 Karta: {user['card']}\n",
                             reply_markup=inline_btn.as_markup())

        await state.clear()
    else:
        await message.answer("Karta Raqamni To'g'ri Kiriting.(8600 1221 1255 1234)")

@dp.message(F.text, SettingsState.full_name)
async def change_user_name(message: types.Message, state: FSMContext):
    is_correct = message.text.split(' ')
    if message.text and len(is_correct) >= 2:
        await db.update_user_name(telegram_id=message.from_user.id, full_name=message.text)
        await message.answer("Ism O'zgartirildi")
        user = await db.select_user(message.from_user.id)
        inline_btn = InlineKeyboardBuilder()
        inline_btn.button(text="👤 Ismni O'zgartirish", callback_data=SettingsCallback(name="change_user_name"))
        inline_btn.button(text="💳 Kartani O'zgartirish", callback_data=SettingsCallback(name="change_user_card"))
        inline_btn.button(text="📞 Telefon Raqamni O'zgartirish",
                          callback_data=SettingsCallback(name="change_user_phone"))
        inline_btn.adjust(1)
        await message.answer(f"👤 Foydalanuvchi: {user['full_name']}\n"
                             f"📞 Telefon: {user['phone']}\n"
                             f"💳 Karta: {user['card']}\n",
                             reply_markup=inline_btn.as_markup())

        await state.clear()
    else:
        await message.answer("Faqat Text Formatda Kamida 2ta so'z bilan yozing")