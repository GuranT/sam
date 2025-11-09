import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers.commands import router as commands_router
from handlers.chat import router as chat_router
from handlers.admin import router as admin_router
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    if not settings.BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен!")
        return
    
    if not settings.DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY не установлен! Бот будет работать в режиме заглушки")
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(commands_router)
    dp.include_router(chat_router)
    dp.include_router(admin_router)
    
    logger.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
