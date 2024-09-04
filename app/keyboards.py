from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.request import get_catalog

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/reg"), KeyboardButton(text="/menu")],
    [KeyboardButton(text="/FAQ"), KeyboardButton(text="/help")],
    [KeyboardButton(text="/contacts")]
], resize_keyboard=True)

back_to_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
])

cancel_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить регистрацию", callback_data="cancel_reg")]
])

num_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить контакт", request_contact=True)]
], resize_keyboard=True)

result_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно", callback_data="success_reg")],
    [InlineKeyboardButton(text="Заполнить форму заново", callback_data="bad_reg")]
])

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    [InlineKeyboardButton(text="Мои заказы", callback_data="show_order")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
])

make_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно", callback_data="add_order")],
    [InlineKeyboardButton(text="Отменить заказ", callback_data="cancel_order")]
])

orders_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить заказ", callback_data="choose_del_order")],
    [InlineKeyboardButton(text="Изменить заказ", callback_data="choose_change_order")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
])

back_to_catalog_with_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
])

back_to_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
])

back_to_show_order = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="К заказам", callback_data="back_to_show_order")]
])


async def to_check_order_keyboard(id: int):
    to_check_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Всё верно", callback_data="to_check_order")],
        [InlineKeyboardButton(text="Ещё раз", callback_data=f"back_to_description_{id}")]
    ])

    return to_check_order_keyboard


async def buy_form(item_id: int):
    buy_form_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оставить заявку", callback_data=f"make_an_order_{item_id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])
    return buy_form_keyboard


async def catalog_keyboard():
    keyboard = InlineKeyboardBuilder()
    catalog = await get_catalog()
    for item in catalog:
        keyboard.add(InlineKeyboardButton(text=f"{item.name}", callback_data=f"catalog_{item.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_catalog"))
    return keyboard.adjust(1).as_markup()


async def back_to_item_info(id: int):
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"back_to_item_info_{id}")]
    ])
    return back_keyboard


async def choose_del_order_keyboard(orders):
    keyboard = InlineKeyboardBuilder()
    for order in orders:
        keyboard.add(InlineKeyboardButton(text=f"{order.id}", callback_data=f"ask_del_order_{order.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_show_order"))
    return keyboard.adjust(2).as_markup()


async def choose_change_order_keyboard(orders):
    keyboard = InlineKeyboardBuilder()
    for order in orders:
        keyboard.add(InlineKeyboardButton(text=f"{order.id}", callback_data=f"ask_change_order_{order.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_show_order"))
    return keyboard.adjust(2).as_markup()


async def del_order(order_num):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтверждаю", callback_data=f"del_order_{order_num}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_show_order")]
    ])
    return keyboard


async def change_order(order_num):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтверждаю", callback_data=f"change_order_{order_num}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_show_order")]
    ])
    return keyboard
