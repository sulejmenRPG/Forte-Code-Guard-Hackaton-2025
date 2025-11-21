# 🚂 Railway Deployment Guide

## ✅ Что я уже сделал (Backend готов):

1. ✅ Подключил PostgreSQL в коде
2. ✅ Создал `Procfile` для Railway
3. ✅ Настроил автосохранение статистики в БД
4. ✅ Добавил `psycopg2-binary` в requirements
5. ✅ Создал `railway.json` с настройками
6. ✅ Подготовил environment variables

---

## 🎯 Твои действия (20-30 минут):

### Шаг 1: Создай GitHub репозиторий (5 минут)

1. **Зайди на GitHub.com**
2. **Создай новый репозиторий:**
   - Название: `ai-code-review-assistant`
   - Public или Private (любое)
   - БЕЗ README, .gitignore

3. **В терминале в папке проекта:**
```bash
git init
git add .
git commit -m "Initial commit - AI Code Review Assistant"
git branch -M main
git remote add origin https://github.com/ТвойЮзернейм/ai-code-review-assistant.git
git push -u origin main
```

---

### Шаг 2: Регистрация на Railway (2 минуты)

1. **Зайди на:** https://railway.app/
2. **Sign up with GitHub** (используй свой GitHub)
3. **Подтверди аккаунт**

---

### Шаг 3: Создай Backend проект (10 минут)

1. **В Railway dashboard:**
   - Нажми **"New Project"**
   - Выбери **"Deploy from GitHub repo"**
   - Выбери свой репозиторий `ai-code-review-assistant`

2. **Railway автоматически:**
   - ✅ Обнаружит Python проект
   - ✅ Установит зависимости из `requirements.txt`
   - ✅ Запустит команду из `Procfile`

3. **Дождись первого деплоя** (~3-5 минут)
   - Будут логи установки пакетов
   - Увидишь "Deployment successful" ✅

---

### Шаг 4: Добавь PostgreSQL (3 минуты)

1. **В твоём проекте на Railway:**
   - Нажми **"New"** → **"Database"** → **"Add PostgreSQL"**

2. **Railway автоматически:**
   - ✅ Создаст БД
   - ✅ Добавит переменную `DATABASE_URL` в твой backend
   - ✅ Перезапустит backend с БД

---

### Шаг 5: Добавь Environment Variables (5 минут)

1. **Зайди в Settings → Variables**

2. **Добавь переменные:**

```
GITLAB_TOKEN=glpat-твой-токен
GEMINI_API_KEY=твой-ключ-gemini
WEBHOOK_SECRET=my_super_secret_123_qwerty
LLM_PROVIDER=gemini
MAX_CODE_LENGTH=50000
ANALYSIS_TIMEOUT=300
MIN_SCORE_FOR_APPROVAL=7.0
AUTO_LABEL_MR=true
```

**ВАЖНО:** `DATABASE_URL` и `PORT` уже есть автоматически от Railway!

3. **Нажми "Deploy"** для перезапуска с новыми переменными

---

### Шаг 6: Получи публичный URL (1 минута)

1. **Settings → Networking**
2. **Generate Domain** или **Add Custom Domain**
3. **Скопируй URL**, например:
   ```
   https://ai-code-review-production.up.railway.app
   ```

4. **Проверь работу:**
   ```
   https://твой-url.railway.app/health
   ```
   
   Должен вернуть:
   ```json
   {
     "status": "healthy",
     "version": "1.0.0",
     "llm_provider": "gemini"
   }
   ```

---

### Шаг 7: Обнови GitLab Webhook (2 минуты)

1. **Зайди в GitLab проект**
2. **Settings → Webhooks**
3. **Измени URL с ngrok на Railway:**
   ```
   Старый: https://shelia-gallic-overchildishly.ngrok-free.dev/webhook/gitlab
   Новый: https://твой-url.railway.app/webhook/gitlab
   ```

4. **Тест webhook** - должно быть ✅

---

## 🎉 ГОТОВО! Backend онлайн!

### Проверка:

✅ Backend: `https://твой-url.railway.app`  
✅ Health: `https://твой-url.railway.app/health`  
✅ Stats: `https://твой-url.railway.app/stats`  
✅ PostgreSQL: Подключена автоматически  

---

## 📊 Далее: Deploy Dashboard

### Шаг 8: Deploy Streamlit Dashboard (опционально)

**Вариант A: Отдельный Railway сервис**

1. **В том же Railway проекте:**
   - New → GitHub Repo (тот же репозиторий)
   - Root Directory: оставь пустым
   - Start Command: `streamlit run dashboard_ru.py --server.port=$PORT --server.address=0.0.0.0`

2. **Environment Variables:**
   ```
   API_URL=https://твой-backend-url.railway.app
   ```

3. **Generate Domain** для dashboard

**Результат:**
- Backend: `https://backend.railway.app`
- Dashboard: `https://dashboard.railway.app`

---

**Вариант B: Streamlit Cloud (бесплатно)**

1. Зайди на https://streamlit.io/cloud
2. Deploy from GitHub
3. Укажи `dashboard_ru.py`
4. Готово!

---

## 💰 Стоимость Railway:

- **$5 бесплатных кредитов/месяц**
- Backend: ~$3-4/месяц
- PostgreSQL: включена в стоимость
- **Хватит на весь хакатон бесплатно!**

---

## 🐛 Troubleshooting:

### Build failed
- Проверь `requirements.txt`
- Убедись что `psycopg2-binary` есть

### Database connection error
- Убедись что PostgreSQL добавлена
- Переменная `DATABASE_URL` должна быть автоматически

### Webhook timeout
- Увеличь `ANALYSIS_TIMEOUT` до 600
- Или используй меньший код для теста

---

## 🚀 Следующие шаги после деплоя:

1. ✅ Создай тестовый MR в GitLab
2. ✅ Проверь что webhook работает
3. ✅ Зайди на `/stats` - должны быть реальные данные из БД
4. ✅ Dashboard покажет статистику из backend API

---

**Готово! Всё онлайн! 🎉**

Нужна помощь? Спроси меня!
