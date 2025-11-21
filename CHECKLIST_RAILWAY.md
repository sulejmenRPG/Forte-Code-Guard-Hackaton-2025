# ✅ Быстрый чеклист для Railway деплоя

## 📋 ЧТО УЖЕ ГОТОВО (я сделал):

- ✅ PostgreSQL интеграция
- ✅ Автосохранение в БД
- ✅ API endpoints для статистики
- ✅ Procfile для Railway
- ✅ railway.json конфиг
- ✅ requirements.txt обновлён
- ✅ Код готов к деплою

---

## 🎯 ТВОЙ ПЛАН (30 минут):

### 1. GitHub (5 мин)
```bash
git init
git add .
git commit -m "Ready for Railway"
git branch -M main
git remote add origin https://github.com/твой-юзернейм/ai-code-review.git
git push -u origin main
```

### 2. Railway.app (2 мин)
- Зайди на https://railway.app/
- Sign up with GitHub
- Подтверди email

### 3. Deploy Backend (10 мин)
- New Project → Deploy from GitHub
- Выбери свой репо
- Дождись деплоя (~5 мин)

### 4. Добавь PostgreSQL (2 мин)
- New → Database → PostgreSQL
- Railway автоматически подключит к backend

### 5. Environment Variables (5 мин)
Settings → Variables → Добавь:
```
GITLAB_TOKEN=твой_токен
GEMINI_API_KEY=твой_ключ
WEBHOOK_SECRET=my_super_secret_123_qwerty
LLM_PROVIDER=gemini
```

### 6. Получи URL (1 мин)
- Settings → Networking → Generate Domain
- Скопируй URL: `https://....railway.app`

### 7. Обнови GitLab Webhook (2 мин)
- GitLab → Settings → Webhooks
- Замени ngrok URL на Railway URL

### 8. Тест (3 мин)
- Создай MR в GitLab
- AI должен оставить комментарий
- Проверь `/stats` - реальные данные!

---

## 🎉 ГОТОВО!

Backend онлайн: `https://твой-url.railway.app`

Статистика теперь РЕАЛЬНАЯ из PostgreSQL! 📊

---

**Подробная инструкция:** `RAILWAY_DEPLOY.md`
