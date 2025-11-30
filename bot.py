import logging
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

CHANNEL_USERNAME = "@temki1win"
ADMIN_USERNAME = "@sazwwww"
WEB_APP_URL = "https://realystycks1.github.io/1win-signalsss/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()

users_db = {}   # user_id : 1win_id


async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False


@router.message(Command("start"))
async def start(message: types.Message):
    sub = await check_sub(message.from_user.id)

    if not sub:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
        ])
        await message.answer(
            f"🚫 Для доступа к боту подпишитесь на канал: {CHANNEL_USERNAME}\n\nПосле нажмите кнопку ниже",
            reply_markup=kb
        )
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎮 Сигналы / Игры", callback_data="games"),
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="📖 Инструкция", callback_data="info"),
            InlineKeyboardButton(text="📩 Связь", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")
        ]
    ])

    await message.answer(
        "✅ Доступ разрешен\n\nВыберите пункт менку:",
        reply_markup=kb
    )


@router.callback_query(lambda call: call.data == "check_sub")
async def recheck(call: types.CallbackQuery):
    sub = await check_sub(call.from_user.id)

    if not sub:
        await call.answer("❌ Вы не подписаны", show_alert=True)
        return

    await start(call.message)
    await call.answer()


@router.callback_query(lambda call: call.data == "profile")
async def profile(call: types.CallbackQuery):
    if call.from_user.id in users_db:
        profile_text = f"👤 Ваш профиль:\n\n🔑 1WIN ID: {users_db[call.from_user.id]}"
    else:
        profile_text = "❗ Введите ваш ID с 1WIN:"

    await call.message.answer(profile_text)
    await call.answer()


@router.message(lambda msg: msg.text.isdigit())
async def save_id(message: types.Message):
    users_db[message.from_user.id] = message.text
    await message.answer("✅ ID сохранён\n\nТеперь вам открыт доступ к сигналам")


@router.callback_query(lambda call: call.data == "games")
async def games(call: types.CallbackQuery):
    if call.from_user.id not in users_db:
        await call.answer("Сначала введите ваш 1WIN ID в профиле", show_alert=True)
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть сигналы", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

    await call.message.answer(
        "🎮 Нажмите кнопку для получения сигналов:",
        reply_markup=kb
    )
    await call.answer()


@router.callback_query(lambda call: call.data == "info")
async def info(call: types.CallbackQuery):
    text = """Бот основан и обучен на кластере нейросети 🖥  
Для тренировки бота было сыграно 🎰10.000+ игр.

В данный момент пользователи бота успешно делают в день 15-25% от своего 💸 капитала!

На текущий момент бот по сей день проходит проверки и исправления!
Точность бота составляет 92%!

Для получения максимального профита следуйте следующей инструкции:

🟢 1. Пройти регистрацию в букмекерской конторе 1WIN

❗ОБЯЗАТЕЛЬНО НУЖНО СОЗДАТЬ НОВЫЙ АККАУНТ❗
(Единственная официальная ссылка на сайт 1WIN находится в канале @temki1win)

Если не открывается - используйте VPN (Швеция)

❗УКАЗАТЬ ПРОМОКОД Sawz500❗

🟢 2. Подключить свой аккаунт к боту (в разделе Профиль)

🟢 3. Пополнить баланс

🟢 4. Зайти в 1win games (Mines / LuckyJet)

🟢 5. Запросить сигнал в боте
"""

    await call.message.answer(text)
    await call.answer()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
