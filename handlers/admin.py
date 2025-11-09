from aiogram import Router, types
from aiogram.filters import Command
from config.settings import settings
from database.user_context import user_manager
from ai.message_processor import get_message_processor
import logging

router = Router()
logger = logging.getLogger(__name__)
message_processor = get_message_processor()

def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return
    
    admin_text = """
🛠 **Панель администратора**

Команды:
/admin_stats - Статистика бота
/admin_broadcast <сообщение> - Рассылка
    """
    await message.answer(admin_text)

@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    stats = f"""
📈 **Статистика бота:**

• Пользователей в кэше: {len(message_processor.user_cache)}
• Активных пользователей: {len(user_manager.users)}
• Запросов за минуту: {len(message_processor.rate_limits)}
• Лимит запросов: {settings.REQUESTS_PER_MINUTE}/мин
    """
    await message.answer(stats)
