"""
Пример плохого кода для демонстрации работы AI Code Review Assistant

Этот файл содержит типичные проблемы, которые AI должен найти:
- SQL injection
- Отсутствие обработки ошибок
- Хардкод паролей
- Неэффективные алгоритмы
"""

import sqlite3


# ❌ ПРОБЛЕМА 1: SQL Injection уязвимость
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Прямая подстановка параметра в SQL - ОПАСНО!
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    return cursor.fetchone()


# ❌ ПРОБЛЕМА 2: Хардкод пароля в коде
def connect_to_database():
    DB_PASSWORD = "admin123"  # Пароль в открытом виде!
    conn = sqlite3.connect('db.sqlite')
    return conn


# ❌ ПРОБЛЕМА 3: Отсутствие обработки ошибок
def process_payment(amount, account_id):
    # Что если account_id не существует?
    # Что если amount отрицательный?
    # Никакой проверки!
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE accounts SET balance = balance - {amount} WHERE id = {account_id}")
    conn.commit()


# ❌ ПРОБЛЕМА 4: Неэффективный алгоритм O(n²)
def find_duplicates(transactions):
    duplicates = []
    for i in range(len(transactions)):
        for j in range(i + 1, len(transactions)):
            if transactions[i] == transactions[j]:
                duplicates.append(transactions[i])
    return duplicates


# ❌ ПРОБЛЕМА 5: Нет логирования критической операции
def transfer_money(from_account, to_account, amount):
    # Перевод денег - критическая операция!
    # Но нигде не логируется
    
    process_payment(amount, from_account)
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE accounts SET balance = balance + {amount} WHERE id = {to_account}")
    conn.commit()


# ❌ ПРОБЛЕМА 6: Раскрытие чувствительной информации
def get_user_info(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Возвращаем ВСЕ данные включая пароль!
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user_data = cursor.fetchone()
    
    return user_data  # Содержит password hash, email, phone и т.д.


# ❌ ПРОБЛЕМА 7: Race condition
balance = 1000

def withdraw(amount):
    global balance
    # Что если два потока одновременно вызовут эту функцию?
    if balance >= amount:
        # Здесь может быть переключение контекста!
        balance -= amount
        return True
    return False


# ❌ ПРОБЛЕМА 8: Слабая валидация
def create_user(username, email, password):
    # Никакой проверки формата email
    # Никакой проверки надежности пароля
    # Никакой проверки на уникальность username
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')")
    conn.commit()


# ❌ ПРОБЛЕМА 9: Утечка ресурсов
def read_transactions():
    file = open('transactions.txt', 'r')
    data = file.read()
    # Забыли закрыть файл!
    return data


# ❌ ПРОБЛЕМА 10: Захардкоженный API ключ
API_KEY = "sk-1234567890abcdef"
SECRET_TOKEN = "my_secret_token_123"

def call_external_api():
    import requests
    response = requests.get(
        "https://api.example.com/data",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    return response.json()
