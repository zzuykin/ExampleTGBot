from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.States import OrderState
import app.keyboards as kb


menu_router = Router()


@menu_router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery, state : FSMContext):
    if await state.get_state() != OrderState.description:
        await state.clear()
        await callback.answer("Каталог")
        await callback.message.edit_text("Каталог 👇👇👇\n",reply_markup=await kb.catalog_keyboard())
    else:
        await callback.answer("Завершите текущий заказ")


@menu_router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery):
    await callback.answer("Назад")
    await callback.message.edit_text("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)
