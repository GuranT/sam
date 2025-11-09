from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🤖 **DeepSeek AI Assistant**\n\n"
        "Доступные команды:\n"
        "/start - начало работы\n"
        "/help - помощь\n"
        "/chat - общение с AI\n\n"
        "Просто напишите сообщение!"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📖 **Помощь:**\n\n"
        "Просто напишите сообщение, и AI ответит!\n"
        "Лимит: 5 запросов в минуту"
    )

@router.message(Command("chat"))
async def cmd_chat(message: types.Message):
    await message.answer("💬 Режим чата активирован! Пишите сообщения...")
