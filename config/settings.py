import os
from dotenv import load_dotenv

load_dotenv()

# Простые настройки без сложных классов
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
ADMIN_IDS = os.getenv('ADMIN_IDS', '123456789')

# Проверка обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")
