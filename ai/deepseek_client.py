import aiohttp
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        
    async def send_message(self, message: str):
        if not self.api_key:
            return "❌ DeepSeek API ключ не настроен"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    headers=headers, 
                    json=payload,
                    timeout=20
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        return f"❌ Ошибка API: {response.status}"
                        
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return "❌ Ошибка соединения. Попробуйте позже."
