from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.models import User
from app.database.request import is_reg, set_user
import app.keyboards as kb
from app.States import Registration

reg_router = Router()


@reg_router.message(Command("reg"))
async def cmd_reg(message: Message, state: FSMContext):
    await state.clear()
    try:
        if await is_reg(message.from_user.id):
            await message.answer("Вы уже зарегестрированы",reply_markup=kb.start_keyboard)
            return
    except:
        print("Errror DataBase")
    await state.clear()
    await state.set_state(Registration.name)
    await message.answer(text="Как вас зовут?", reply_markup=kb.cancel_registration)


@reg_router.callback_query(F.data == "registration")
async def cmd_reg(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Регистрация")
    await state.clear()
    await state.set_state(Registration.name)
    await callback.message.edit_text(text="Как вас зовут?", reply_markup=kb.cancel_registration)



@reg_router.message(Registration.name)
async def reg_first(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.number)
    await message.answer("Введите номер телефона или отправьте контакт", reply_markup=kb.num_keyboard)


@reg_router.message(Registration.number)
async def reg_second(message: Message, state: FSMContext):
    if message.content_type == ContentType.CONTACT:
        phone_number = message.contact.phone_number
    else:
        if not message.text.isdigit():
            await message.answer("Пожалуйста, введите только цифры.", reply_markup=kb.num_keyboard)
            return
        if len(message.text) != 11:
            await message.answer("Неверное колличество цифр в номере.", reply_markup=kb.num_keyboard)
            return
        phone_number = message.text
    await state.update_data(number=phone_number)
    await state.set_state(Registration.mail)
    await message.answer("Введите свой mail.", reply_markup=ReplyKeyboardRemove())


@reg_router.message(Registration.mail)
async def reg_third(message: Message, state: FSMContext):
    if not all(x in message.text for x in ("@", ".")):
        await message.answer("Некорректный e-mail, попробуйте ещё раз", reply_markup=kb.cancel_registration)
        return
    await state.update_data(mail=message.text)
    await state.update_data(username=message.from_user.username)
    await state.update_data(id=message.from_user.id)
    data = await state.get_data()
    await message.answer(f"Проверьте свои данные! \n"
                         f"Ваше имя: {data['name']}\n"
                         f"Номер телефона: {data['number']}\n"
                         f"E-mail: {data['mail']}"
                         , reply_markup=kb.result_reg)


@reg_router.callback_query(F.data == "success_reg")
async def save_registered(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = User(
        tg_id=data['id'],
        name=data['name'],
        user_name=data['username'],
        email=data['mail'],
        phone_num=data['number']
    )
    await set_user(user)
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Регистрация была завершена!")
    await callback.message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)


@reg_router.callback_query(F.data == "bad_reg")
async def bad_reg(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Заполняем форму заново")
    await cmd_reg(callback.message, state)


@reg_router.callback_query(F.data == "cancel_reg")
async def cancel_reg(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Регистрация была отменена", show_alert=True)
    await callback.message.answer("Регистрация была отменена", reply_markup=ReplyKeyboardRemove())
    await callback.message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)
