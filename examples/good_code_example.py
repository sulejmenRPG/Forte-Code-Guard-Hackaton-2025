"""
Пример хорошего кода - как должно быть исправлено

AI Code Review Assistant должен рекомендовать такие исправления
"""

import sqlite3
import os
import logging
from typing import Optional, Dict, List
from contextlib import contextmanager
import hashlib
import re
from threading import Lock

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ✅ ИСПРАВЛЕНИЕ 1: Параметризованные SQL запросы
def get_user(user_id: int) -> Optional[Dict]:
    """Получить пользователя по ID безопасным способом"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Используем параметризованный запрос
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        return None


# ✅ ИСПРАВЛЕНИЕ 2: Пароли в переменных окружения
@contextmanager
def get_db_connection():
    """Context manager для безопасной работы с БД"""
    db_password = os.getenv('DB_PASSWORD')  # Из переменной окружения
    if not db_password:
        raise ValueError("DB_PASSWORD not set in environment")
    
    conn = None
    try:
        conn = sqlite3.connect('db.sqlite')
        yield conn
    finally:
        if conn:
            conn.close()


# ✅ ИСПРАВЛЕНИЕ 3: Полная валидация и обработка ошибок
def process_payment(amount: float, account_id: int) -> bool:
    """
    Обработать платеж с валидацией
    
    Args:
        amount: Сумма платежа
        account_id: ID аккаунта
        
    Returns:
        bool: Успешность операции
    """
    # Валидация входных данных
    if amount <= 0:
        logger.error(f"Invalid amount: {amount}")
        return False
    
    if account_id <= 0:
        logger.error(f"Invalid account_id: {account_id}")
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Проверяем существование аккаунта
            cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
            result = cursor.fetchone()
            
            if not result:
                logger.error(f"Account {account_id} not found")
                return False
            
            balance = result[0]
            
            # Проверяем достаточность средств
            if balance < amount:
                logger.warning(f"Insufficient funds for account {account_id}")
                return False
            
            # Выполняем операцию
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, account_id)
            )
            conn.commit()
            
            logger.info(f"Payment processed: {amount} from account {account_id}")
            return True
            
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return False


# ✅ ИСПРАВЛЕНИЕ 4: Эффективный алгоритм O(n)
def find_duplicates(transactions: List) -> List:
    """Найти дубликаты эффективно используя set"""
    seen = set()
    duplicates = []
    
    for transaction in transactions:
        if transaction in seen and transaction not in duplicates:
            duplicates.append(transaction)
        seen.add(transaction)
    
    return duplicates


# ✅ ИСПРАВЛЕНИЕ 5: Логирование критических операций
def transfer_money(from_account: int, to_account: int, amount: float) -> bool:
    """
    Перевести деньги между аккаунтами с логированием
    
    Логируются все операции для audit trail
    """
    logger.info(f"Transfer initiated: {amount} from {from_account} to {to_account}")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Используем транзакцию для атомарности
            conn.execute("BEGIN TRANSACTION")
            
            # Списание
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?",
                (amount, from_account, amount)
            )
            
            if cursor.rowcount == 0:
                conn.rollback()
                logger.error(f"Transfer failed: insufficient funds or account not found")
                return False
            
            # Зачисление
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_account)
            )
            
            if cursor.rowcount == 0:
                conn.rollback()
                logger.error(f"Transfer failed: recipient account {to_account} not found")
                return False
            
            conn.commit()
            logger.info(f"Transfer completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Transfer error: {str(e)}")
        return False


# ✅ ИСПРАВЛЕНИЕ 6: Возвращаем только нужные данные
def get_user_info(username: str) -> Optional[Dict]:
    """Получить публичную информацию о пользователе"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Выбираем только нужные поля
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username = ?",
                (username,)
            )
            
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2]
                    # НЕТ password, phone и других чувствительных данных
                }
            return None
            
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        return None


# ✅ ИСПРАВЛЕНИЕ 7: Thread-safe операции
class BankAccount:
    """Thread-safe банковский аккаунт"""
    
    def __init__(self, initial_balance: float = 0):
        self.balance = initial_balance
        self._lock = Lock()
    
    def withdraw(self, amount: float) -> bool:
        """Потокобезопасное снятие средств"""
        with self._lock:  # Блокировка для атомарности
            if self.balance >= amount:
                self.balance -= amount
                logger.info(f"Withdrawn {amount}, new balance: {self.balance}")
                return True
            logger.warning(f"Insufficient funds: {self.balance} < {amount}")
            return False


# ✅ ИСПРАВЛЕНИЕ 8: Валидация входных данных
def validate_email(email: str) -> bool:
    """Проверить формат email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """Проверить надежность пароля"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True


def hash_password(password: str) -> str:
    """Хешировать пароль"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, email: str, password: str) -> bool:
    """
    Создать пользователя с полной валидацией
    """
    # Валидация
    if not username or len(username) < 3:
        logger.error("Invalid username")
        return False
    
    if not validate_email(email):
        logger.error("Invalid email format")
        return False
    
    if not validate_password(password):
        logger.error("Weak password")
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Проверка уникальности
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                logger.error(f"Username {username} already exists")
                return False
            
            # Хешируем пароль перед сохранением
            password_hash = hash_password(password)
            
            # Безопасная вставка
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            
            logger.info(f"User {username} created successfully")
            return True
            
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return False


# ✅ ИСПРАВЛЕНИЕ 9: Context manager для файлов
def read_transactions() -> str:
    """Читать транзакции с автоматическим закрытием файла"""
    try:
        with open('transactions.txt', 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        logger.error("Transactions file not found")
        return ""
    except Exception as e:
        logger.error(f"Error reading transactions: {str(e)}")
        return ""


# ✅ ИСПРАВЛЕНИЕ 10: Секреты в переменных окружения
def call_external_api() -> Optional[Dict]:
    """Вызвать внешний API безопасно"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API_KEY not set in environment")
        return None
    
    try:
        import requests
        response = requests.get(
            "https://api.example.com/data",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10  # Добавили timeout
        )
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        logger.error(f"API call failed: {str(e)}")
        return None
