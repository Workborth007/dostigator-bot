import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging
import os

# Вставь сюда свой токен
BOT_TOKEN = "7751726615:AAGQQ6KpVykBTfDytrEbArUZwWmx6Rc0RPc"

# Включаем логирование (чтобы видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=types.ParseMode.MARKDOWN)
)
dp = Dispatcher()

# --- КНОПКИ ---
def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить цель", callback_data="add_goal")
    builder.button(text="📋 Мои цели", callback_data="view_goals")
    builder.button(text="✅ Выполнить задачу", callback_data="complete_goal")
    builder.button(text="🗑 Удалить цель", callback_data="delete_goal")
    return builder.as_markup()

# --- ОБРАБОТЧИКИ ---
user_goals = {}  # Словарь для хранения целей пользователей

@dp.message()
async def start_handler(message: types.Message):
    if message.text == "/start":
        await message.answer(
            "👋 Привет! Я твой помощник по целям и задачам!\n\nВыбирай действие:",
            reply_markup=main_menu_keyboard()
        )

@dp.callback_query()
async def menu_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "add_goal":
        await callback.message.answer("📝 Введите новую цель:")
        dp.message.register(lambda msg: add_goal(msg, user_id))

    elif callback.data == "view_goals":
        goals = user_goals.get(user_id, [])
        if goals:
            await callback.message.answer(
                "📋 Твои цели:\n" + "\n".join(f"- {goal}" for goal in goals)
            )
        else:
            await callback.message.answer("📭 У тебя пока нет целей.")

    elif callback.data == "complete_goal":
        await callback.message.answer("✅ Введите номер цели, которую выполнили:")
        dp.message.register(lambda msg: complete_goal(msg, user_id))

    elif callback.data == "delete_goal":
        await callback.message.answer("🗑 Введите номер цели для удаления:")
        dp.message.register(lambda msg: delete_goal(msg, user_id))

async def add_goal(message: types.Message, user_id: int):
    goal = message.text.strip()
    user_goals.setdefault(user_id, []).append(goal)
    await message.answer("🎯 Цель добавлена!", reply_markup=main_menu_keyboard())

async def complete_goal(message: types.Message, user_id: int):
    try:
        num = int(message.text.strip()) - 1
        goals = user_goals.get(user_id, [])
        if 0 <= num < len(goals):
            goal = goals.pop(num)
            await message.answer(f"✅ Поздравляю! Ты выполнил цель: {goal}")
        else:
            await message.answer("🚫 Неверный номер цели.")
    except Exception as e:
        await message.answer("⚠ Ошибка: введите номер.")

    await message.answer("Выбирай следующее действие:", reply_markup=main_menu_keyboard())

async def delete_goal(message: types.Message, user_id: int):
    try:
        num = int(message.text.strip()) - 1
        goals = user_goals.get(user_id, [])
        if 0 <= num < len(goals):
            goal = goals.pop(num)
            await message.answer(f"🗑 Цель удалена: {goal}")
        else:
            await message.answer("🚫 Неверный номер цели.")
    except Exception as e:
        await message.answer("⚠ Ошибка: введите номер.")

    await message.answer("Выбирай следующее действие:", reply_markup=main_menu_keyboard())

# --- ОСНОВНОЙ ЗАПУСК ---
async def main():
    # Установка команд бота в интерфейсе Telegram
    await bot.set_my_commands([
        BotCommand(command="/start", description="Запустить бота 🎯"),
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
