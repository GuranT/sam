import re
import logging
from cachetools import TTLCache
from ai.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

# Глобальный экземпляр для избежания циклических импортов
_message_processor_instance = None

def get_message_processor():
    global _message_processor_instance
    if _message_processor_instance is None:
        _message_processor_instance = MessageProcessor()
    return _message_processor_instance

class MessageProcessor:
    def __init__(self):
        self.deepseek = DeepSeekClient()
        self.user_cache = TTLCache(maxsize=1000, ttl=3600)  # Кэш на 1 час
        self.rate_limits = TTLCache(maxsize=1000, ttl=60)   # Лимы на 1 минуту
    
    def _check_rate_limit(self, user_id: int) -> bool:
        """Проверка лимита запросов"""
        current = self.rate_limits.get(user_id, 0)
        if current >= 10:  # 10 запросов в минуту
            return False
        self.rate_limits[user_id] = current + 1
        return True
    
    def _sanitize_message(self, text: str) -> str:
        """Очистка сообщения от потенциально опасного контента"""
        # Удаляем слишком длинные последовательности символов
        text = re.sub(r'(.)\1{10,}', r'\1\1\1', text)
        # Обрезаем слишком длинные сообщения
        if len(text) > 4000:
            text = text[:4000] + "..."
        return text.strip()
    
    async def process_message(self, user_id: int, message: str, mode: str = "assistant") -> str:
        """Обработка сообщения пользователя"""
        
        # Проверяем лимит запросов
        if not self._check_rate_limit(user_id):
            return "⚠️ Слишком много запросов. Подождите минуту."
        
        # Очищаем сообщение
        sanitized_message = self._sanitize_message(message)
        
        if not sanitized_message:
            return "Пожалуйста, введите осмысленное сообщение."
        
        # Добавляем промпт в зависимости от режима
        prompts = {
            "assistant": "Ты полезный AI ассистент. Отвечай вежливо и информативно.",
            "developer": "Ты AI помощник для разработчиков. Помогай с кодом, объясняй концепции программирования.",
            "creative": "Ты креативный AI помощник. Помогай с творческими задачами, генерируй идеи.",
            "quick": "Давай краткие и точные ответы без лишних деталей."
        }
        
        system_prompt = prompts.get(mode, prompts["assistant"])
        
        # Получаем историю сообщений из кэша
        history = self.user_cache.get(user_id, [])
        history.append({"role": "system", "content": system_prompt})
        
        try:
            # Отправляем запрос в DeepSeek
            response = await self.deepseek.send_message(
                sanitized_message, 
                history
            )
            
            # Обновляем историю в кэше
            user_history = [
                {"role": "user", "content": sanitized_message},
                {"role": "assistant", "content": response}
            ]
            self.user_cache[user_id] = user_history[-6:]  # Храним последние 3 пары сообщений
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "❌ Произошла ошибка при обработке запроса. Попробуйте еще раз."
    
    def clear_user_history(self, user_id: int):
        """Очистка истории пользователя"""
        if user_id in self.user_cache:
            del self.user_cache[user_id]
        if user_id in self.rate_limits:
            del self.rate_limits[user_id]
