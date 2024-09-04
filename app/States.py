from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    number = State()
    mail = State()


class OrderState(StatesGroup):
    description = State()


class ChangeOrderState(StatesGroup):
    change_description = State()
