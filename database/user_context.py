from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class UserContext:
    user_id: int
    current_mode: str = "assistant"
    message_count: int = 0
    is_active: bool = True

class UserManager:
    def __init__(self):
        self.users: Dict[int, UserContext] = {}
    
    def get_user(self, user_id: int) -> UserContext:
        """Получение или создание контекста пользователя"""
        if user_id not in self.users:
            self.users[user_id] = UserContext(user_id=user_id)
        return self.users[user_id]
    
    def update_user_mode(self, user_id: int, mode: str):
        """Обновление режима пользователя"""
        user = self.get_user(user_id)
        user.current_mode = mode
    
    def increment_message_count(self, user_id: int):
        """Увеличение счетчика сообщений"""
        user = self.get_user(user_id)
        user.message_count += 1
    
    def clear_user_data(self, user_id: int):
        """Очистка данных пользователя"""
        if user_id in self.users:
            del self.users[user_id]

# Глобальный экземпляр
user_manager = UserManager()
