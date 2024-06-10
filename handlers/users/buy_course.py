import os
from loader import dp, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from keyboards.default.register import course_button, main_button
from states.all import BuyCourseState
from environs import Env

env = Env()
env.read_env()


def parse_telegram_message(message):
    if message is not None:
        message = message.replace("<p>", "")
        if message.endswith("</p>"):
            message = message[:-4]
        for i in ["</p>", "<br>", "<br/>", "<br />"]:
            message = message.replace(i, "\n")
        message = message.replace("&nbsp;", " ")
    return message


class CourseCallback(CallbackData, prefix="ikb0001"):
    course_id: int


@dp.message(F.text == '📚 Kurslar')
async def courses(message: types.Message, state: FSMContext):
    await message.answer('Kurslarimizdan birini tanlang', reply_markup=await course_button())
    await state.set_state(BuyCourseState.select)


@dp.message(F.text, BuyCourseState.select)
async def select_course(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Bosh Menu":
        await message.answer("Bosh Menu", reply_markup=main_button())
        await state.clear()
    else:
        course = await db.select_course_by_title(title=message.text)
        extension = os.path.splitext(course['content'])[1].lower()
        content = parse_telegram_message(course['text'])
        buy_inline_button = InlineKeyboardBuilder()
        buy_inline_button.button(text="✅ Sotib olish", callback_data=CourseCallback(course_id=course['id']))

        if course['file_id'] and extension in ['.jpg', '.jpeg', '.png']:
            await state.update_data({"course": course})
            await message.answer_photo(photo=course['file_id'],
                                       caption=content,
                                       parse_mode="HTML",
                                       reply_markup=buy_inline_button.as_markup())

            # await state.set_state(BuyCourseState.buy)
        elif course['file_id'] and extension in ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.webm', '.webm.part']:
            await state.update_data({"course": course})
            await message.answer_video(video=course['file_id'],
                                       caption=content,
                                       parse_mode="HTML",
                                       reply_markup=buy_inline_button.as_markup())
        elif not course['file_id'] and extension in ['.jpg', '.jpeg', '.png']:
            file_path = f"src/media/{course['content']}"
            try:
                photo = FSInputFile(file_path)
                response = await message.answer_photo(photo,
                                                      caption=content,
                                                      parse_mode="HTML",
                                                      reply_markup=buy_inline_button.as_markup())
                await db.update_course_file_id(response.photo[-1].file_id, course['id'])

            except Exception as e:
                await message.answer(f"Failed to send image: {str(e)}\n\n"
                                     f"Please contact the admin for assistance.")
        elif not course['file_id'] and extension in ['.mp4', '.avi', '.mkv', '.mov', '.mp3', '.webm', '.webm.part']:
            file_path = f"src/media/{course['content']}"
            try:
                video = FSInputFile(file_path)
                response = await message.answer_video(video,
                                                      caption=content,
                                                      parse_mode="HTML",
                                                      reply_markup=buy_inline_button.as_markup())
                await db.update_course_file_id(response.video.file_id, course['id'])
            except Exception as e:
                await message.answer(f"Failed to send video: {str(e)}\n\n"
                                     f"Please contact the admin for assistance.")


@dp.callback_query(CourseCallback.filter(), BuyCourseState.select)
async def change_language(call: types.CallbackQuery, callback_data: CourseCallback, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    course_id = callback_data.course_id
    print(course_id)
    # await db.add_user_course(user_id=call.from_user.id, course_id=course["id"])
    # await call.message.answer("Kurs sotib olindi", reply_markup=main_button())
