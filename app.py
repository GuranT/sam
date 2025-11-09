import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers.commands import router as commands_router
from handlers.chat import router as chat_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Получаем настройки из переменных окружения
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не установлен!")
        return
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(commands_router)
    dp.include_router(chat_router)
    
    logger.info("🤖 Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
