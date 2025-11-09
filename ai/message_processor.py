import re
import logging
from cachetools import TTLCache
from ai.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

def get_message_processor():
    return MessageProcessor()

class MessageProcessor:
    def __init__(self):
        self.deepseek = DeepSeekClient()
        self.user_cache = TTLCache(maxsize=500, ttl=1800)  # Уменьшено
        self.rate_limits = TTLCache(maxsize=500, ttl=60)
    
    def _check_rate_limit(self, user_id: int) -> bool:
        current = self.rate_limits.get(user_id, 0)
        if current >= 5:  # Уменьшено
            return False
        self.rate_limits[user_id] = current + 1
        return True
    
    def _sanitize_message(self, text: str) -> str:
        if len(text) > 2000:  # Уменьшено
            text = text[:2000] + "..."
        return text.strip()
    
    async def process_message(self, user_id: int, message: str, mode: str = "assistant") -> str:
        if not self._check_rate_limit(user_id):
            return "⚠️ Слишком много запросов. Подождите минуту."
        
        sanitized_message = self._sanitize_message(message)
        
        if not sanitized_message:
            return "Пожалуйста, введите осмысленное сообщение."
        
        try:
            response = await self.deepseek.send_message(sanitized_message)
            return response
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "❌ Произошла ошибка. Попробуйте еще раз."
    
    def clear_user_history(self, user_id: int):
        if user_id in self.user_cache:
            del self.user_cache[user_id]
        if user_id in self.rate_limits:
            del self.rate_limits[user_id]
