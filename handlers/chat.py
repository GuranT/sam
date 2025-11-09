from aiogram import Router, types
from ai.message_processor import MessageProcessor
import os
import logging

router = Router()
logger = logging.getLogger(__name__)

# Создаем процессор сообщений
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
message_processor = MessageProcessor(DEEPSEEK_API_KEY) if DEEPSEEK_API_KEY else None

@router.message()
async def handle_all_messages(message: types.Message):
    if message.text.startswith('/'):
        return
    
    if not message_processor:
        await message.answer("❌ AI не настроен. Проверьте DEEPSEEK_API_KEY")
        return
    
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        response = await message_processor.process_message(
            message.from_user.id, 
            message.text
        )
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await message.answer("❌ Ошибка обработки сообщения")
