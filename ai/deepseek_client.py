import aiohttp
import json
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.DEEPSEEK_MODEL
        
    async def send_message(self, message: str, conversation_history: list = None):
        """Отправка сообщения в DeepSeek API"""
        if not self.api_key:
            raise ValueError("DeepSeek API ключ не настроен")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = []
        
        # Добавляем историю сообщений
        if conversation_history:
            messages.extend(conversation_history[-settings.MAX_HISTORY:])
        
        # Добавляем текущее сообщение
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": settings.MAX_TOKENS,
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    headers=headers, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API error: {response.status} - {error_text}")
                        return f"Ошибка API: {response.status}"
                        
        except Exception as e:
            logger.error(f"Exception in DeepSeek API call: {str(e)}")
            return "Извините, произошла ошибка при обращении к AI. Попробуйте позже."

    async def get_models(self):
        """Получение доступных моделей"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.deepseek.com/v1/models",
                headers=headers
            ) as response:
                return await response.json()
