from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.database.request import (get_item, is_reg, get_user, set_order, get_orders,
                                  get_items_name, del_order, get_order, change_order)
from aiogram.fsm.context import FSMContext
from app.States import OrderState, ChangeOrderState
from app.database.models import Order
import app.keyboards as kb

order_router = Router()


@order_router.callback_query(F.data.startswith("back_to_item_info_"))  # !!!!!
@order_router.callback_query(F.data.startswith("catalog_"))
async def item_telegram(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith("back_to_item_info_"):
        await callback.message.delete()
        await state.clear()
    data = await state.get_data()
    if len(data) >= 1 or await state.get_state() == OrderState.description:
        await callback.answer("Завершите текущий заказ", show_alert=True)
        return
    item = await get_item(int(callback.data.split("_")[-1]))
    await callback.answer(item.name)
    await callback.message.answer_photo(item.photo_url, caption=f"{item.name}\n \n {item.description}",
                                        reply_markup=await kb.buy_form(item.id))


@order_router.callback_query(F.data.startswith("back_to_description_"))
@order_router.callback_query(F.data.startswith("make_an_order_"))
async def order_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    data = await state.get_data()
    if len(data) >= 1:
        await callback.answer("Завершите текущий заказ", show_alert=True)
        return
    if not await is_reg(callback.from_user.id):
        await callback.answer("Вы не зарегистрированы", show_alert=True)
        await callback.message.answer("Вы не зарегистрированы", reply_markup=kb.back_to_catalog_with_reg)
        return
    item = await get_item(int(callback.data.split("_")[-1]))
    await state.update_data(item=item.id)
    await state.set_state(OrderState.description)
    await callback.message.answer(f"Отлично! \n Пожалуйста, напишите краткое описание и желаемый резульат"
                                  f" для услуги {item.name}:",
                                  reply_markup=await kb.back_to_item_info(item.id))


@order_router.message(OrderState.description)
async def order_info_description(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(f"Ваше описание верное? Или хотите заполнить ещё раз?\n"
                         f"{message.text}", reply_markup=await kb.to_check_order_keyboard(data['item']))


@order_router.callback_query(F.data == "to_check_order")
async def check_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if await state.get_state() != OrderState.description:
        await callback.message.delete()
        await callback.message.answer("Начните новый заказ")
        return
    data = await state.get_data()
    item = await get_item(data['item'])
    text = f"Проверьте правильность заказа :\n" \
           f"Услуга: {item.name}\n" \
           f"Описание: {data['description']}"
    await callback.message.edit_text(text, reply_markup=kb.make_order)


@order_router.callback_query(F.data == "add_order")
async def add_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    user = await get_user(callback.from_user.id)
    order = Order(
        user_id=user.id,
        item_id=data['item'],
        user_description=data['description']
    )
    await set_order(order)
    await state.clear()
    await callback.message.edit_text("Вы успешно создали заказ")
    await callback.message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)


@order_router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("Вы отменили заказ")
    await callback.message.answer("Команды 👇👇👇",reply_markup=kb.start_keyboard)


@order_router.callback_query(F.data == "back_to_show_order")
@order_router.callback_query(F.data == "show_order")
async def show_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if not await is_reg(callback.from_user.id):
        await callback.answer("Вы не зарегистрированы", show_alert=True)
        await callback.message.edit_text("Вы не зарегистрированы", reply_markup=kb.back_to_catalog_with_reg)
        return
    if await state.get_state() == OrderState.description:
        await callback.answer("Завершите текущий заказ")
        return
    await callback.answer()
    orders = await get_orders(callback.from_user.id)
    if len(orders) == 0:
        await callback.message.edit_text("У вас ещё нет заказов 😥", reply_markup=kb.back_to_catalog)
        return
    item_names = await get_items_name()
    text = "Ваши заказы:\n"
    for i in range(len(orders)):
        text += f" ☑️Заказ номер {orders[i].id}. {item_names[orders[i].item_id]}. Описание:\n" \
                f"{orders[i].user_description}\n"
    await state.update_data(mes=text)
    await state.update_data(orders=orders)
    await callback.message.edit_text(text, reply_markup=kb.orders_keyboard)


# del
@order_router.callback_query(F.data == "choose_del_order")
async def choose_del_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Удалить заказ")
    data = await state.get_data()
    await callback.message.edit_text(text=data['mes'] + "\n Какой заказ вы хотите отменить? 👇👇👇",
                                     reply_markup=await kb.choose_del_order_keyboard(data['orders']))


@order_router.callback_query(F.data.startswith("ask_del_order_"))
async def ask_to_del_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    order_id = callback.data.split("_")[-1]
    data = await state.get_data()
    await callback.message.edit_text(text=f"Вы уверены, что хотите удалить заказ {order_id}?\n"
                                          f"{data['mes']}", reply_markup=await kb.del_order(order_id))


@order_router.callback_query(F.data.startswith("del_order_"))
async def del_order_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await del_order(callback.data.split("_")[-1])
    await state.clear()
    await callback.message.edit_text("Вы успешно удалили заказ", reply_markup=kb.back_to_show_order)
    await callback.message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)


# choose
@order_router.callback_query(F.data == "choose_change_order")
async def choose_change_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Изменить заказ")
    data = await state.get_data()
    await callback.message.edit_text(text=data['mes'] + "\n Какой заказ вы хотите изменить? 👇👇👇",
                                     reply_markup=await kb.choose_change_order_keyboard(data['orders']))


@order_router.callback_query(F.data.startswith("ask_change_order_"))
async def ask_change_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Изменить заказ")
    await state.set_state(ChangeOrderState.change_description)
    await state.update_data(order_id=int(callback.data.split('_')[-1]))
    await callback.message.edit_text(f"Внестите измение в описание заказа {callback.data.split('_')[-1]}:")


@order_router.message(ChangeOrderState.change_description)
async def confirm_change(message: Message, state: FSMContext):
    await state.update_data(update_desc=message.text)
    data = await state.get_data()
    order = await get_order(data['order_id'])
    item = await get_item(order.item_id)
    await message.answer(f"Ваш заказ номер {order.id}: {item.name}:\n"
                         f"{message.text}", reply_markup=await kb.change_order(order.id))


@order_router.callback_query(F.data.startswith("change_order_"))
async def change_order_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await change_order(data['order_id'], data['update_desc'])
    await state.clear()
    await callback.message.edit_text("Вы успешно изменили заказ", reply_markup=kb.back_to_show_order)
    await callback.message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)
    await state.clear()
