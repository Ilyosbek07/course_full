from aiogram.filters.state import State, StatesGroup


class Withdraw(StatesGroup):
    withdraw = State()


class SettingsState(StatesGroup):
    full_name = State()
    phone = State()
    card = State()


class BuyCourseState(StatesGroup):
    select = State()
    buy = State()


class RegisterState(StatesGroup):
    full_name = State()
    phone_number = State()
    is_agree = State()
    card = State()
    collect_data = State()
