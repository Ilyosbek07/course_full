from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from loader import db


def admin_button():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="🗣 Reklama yuborish"),
        KeyboardButton(text="📊 Obunachilar soni"),
    )
    button.row(
        KeyboardButton(text="🗣 Kanal qo'shish"), KeyboardButton(text="🗣 Kanallar")
    )
    button.adjust(2, 2)
    return button.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang!",
    )


def main_button():
    button = ReplyKeyboardBuilder()
    button.add(
        KeyboardButton(text="Tekshirish"),
        # KeyboardButton(text="📚 Kurslar"),
    )
    button.add(
        # KeyboardButton(text="♻️ Kursni Ulashish"),
        KeyboardButton(text="♻️ Ulashish Posti"),
        KeyboardButton(text="⚙️ Sozlamalar"),
    )
    # button.add(
    #     KeyboardButton(text="💸 Hisobim"),
    # )
    # button.add(
    #     KeyboardButton(text="🔥 Boost 2X")
    # )
    button.adjust(1)
    return button.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang!",
    )


async def course_button():
    courses = await db.select_all_courses()
    button = ReplyKeyboardBuilder()
    button.add(KeyboardButton(text="⬅️ Bosh Menu"))

    for course in courses:
        button.row(KeyboardButton(text=course["title"]))
    button.adjust(1,2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)


def number_button():
    button = ReplyKeyboardBuilder()

    button.row(KeyboardButton(text="📲 Ramani Yuborish", request_contact=True))
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)


def agree_button():
    button = ReplyKeyboardBuilder()

    button.row(KeyboardButton(text="✅ Roziman"))
    button.adjust(2)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)
