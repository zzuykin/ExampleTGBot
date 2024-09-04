from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
import app.keyboards as kb

main_router = Router()


@main_router.message(CommandStart())
async def cmd_start(message: Message):
    intro_message = f"Привет! {message.from_user.first_name} {message.from_user.last_name} Я — бот BuyMyBot, и моя задача — помочь вам с созданием уникальных ботов и сайтов." \
                    f" Если вам нужен профессиональный бот или сайт для вашего бизнеса, вы обратились по адресу. " \
                    f"Напишите мне, и я расскажу, как мы можем вам помочь! \n👇👇👇"
    await message.answer(text=intro_message, reply_markup=kb.start_keyboard)


@main_router.message(Command('help'))
async def cmd_help(message: Message):
    help_message = (
        "🛠️ *Команды, доступные в этом боте:*\n\n"
        "1️⃣ `/start` — Запуск бота и приветственное сообщение.\n"
        "2️⃣ `/help` — Выводит это сообщение с информацией о командах.\n"
        "3️⃣ `/menu` - меню бота. \n"
        "4️⃣` /FAQ` - часто задаваемые вопросы\n"
        "5️⃣ `/reg` — Регистрация в системе. Обязательна для оформления заказов.\n"
        "6️⃣` /contacts` — Связаться с разработчиком для вопросов и предложений.\n\n"
        "📌 *Примечание:* Все заказы можно оформить только после регистрации."
    )
    await message.answer(text=help_message, reply_markup=kb.back_to_start)


@main_router.message(Command('FAQ'))
async def cmd_FAQ(message: Message):
    faq_message = (
        "❓ *Часто задаваемые вопросы:*\n\n"
        "🔹 *Вопрос:* Какие гарантии вы предоставляете на свои услуги?\n"
        "🔸 *Ответ:* Мы предоставляем гарантию на исправление любых багов и ошибок, обнаруженных в течение 30 дней после сдачи проекта.\n\n"
        "🔹 *Вопрос:* Как проходит процесс создания бота или сайта?\n"
        "🔸 *Ответ:* После регистрации и оформления заказа, мы обсуждаем ваши требования и пожелания. Затем начинается разработка, по окончании которой вы получите готовый продукт на проверку.\n\n"
        "🔹 *Вопрос:* Сколько времени занимает разработка?\n"
        "🔸 *Ответ:* Время разработки зависит от сложности проекта. В среднем, создание бота занимает 1-2 недели, а сайта — до 4 недель.\n\n"
        "🔹 *Вопрос:* Какие формы оплаты вы принимаете?\n"
        "🔸 *Ответ:* Мы принимаем оплату через банковские карты, электронные кошельки и переводы на расчетный счет.\n\n"
        "📩 *Если у вас остались вопросы, не стесняйтесь связаться с нами через команду* `/contact`."
    )
    await message.answer(text=faq_message, reply_markup=kb.back_to_start)


@main_router.message(Command('contacts'))
async def cmd_contact(message: Message):
    contact_text = f"📬 Наш мейл: example_email@gmail.com\n \n" \
                   f"📱 Наш телефон: +7 (999)-999-99-99"
    await message.answer(text=contact_text, reply_markup=kb.back_to_start)


@main_router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer("👇👇👇 Меню 👇👇👇", reply_markup=kb.menu_keyboard)


@main_router.callback_query(F.data == "back_to_start")
async def back_from_cmd_start(callback: CallbackQuery):
    await callback.answer("Назад")
    await callback.message.delete()
