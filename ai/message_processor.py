import logging
from cachetools import TTLCache
from ai.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

class MessageProcessor:
    def __init__(self, deepseek_api_key: str):
        self.deepseek = DeepSeekClient(deepseek_api_key)
        self.rate_limits = TTLCache(maxsize=500, ttl=60)
    
    def _check_rate_limit(self, user_id: int) -> bool:
        current = self.rate_limits.get(user_id, 0)
        if current >= 5:
            return False
        self.rate_limits[user_id] = current + 1
        return True
    
    async def process_message(self, user_id: int, message: str) -> str:
        if not self._check_rate_limit(user_id):
            return "⚠️ Слишком много запросов. Подождите минуту."
        
        if not message.strip():
            return "Пожалуйста, введите сообщение."
        
        try:
            response = await self.deepseek.send_message(message)
            return response
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return "❌ Ошибка. Попробуйте еще раз."
