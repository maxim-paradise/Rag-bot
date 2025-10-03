# Руководство по настройке Frontend

## Быстрый старт

### 1. Переключение версии Node.js

Проект требует Node.js версии **20.19+** или **22.12+**.

```bash
# Проверьте текущую версию
node --version

# Переключитесь на подходящую версию через nvm
nvm use 22.12.0

# Если версия не установлена
nvm install 22.12.0
nvm use 22.12.0
```

### 2. Установка зависимостей

```bash
# Перейдите в папку frontend
cd front

# Установите зависимости
npm install
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне папки `front/`:

```env
BACKEND_URL=http://localhost:8000
PUBLIC_APP_NAME=AI Chatbot RAG
PUBLIC_APP_VERSION=1.0.0
```

### 4. Запуск приложения

```bash
# Development режим
npm run dev

# Откроется на http://localhost:5173
```

## Что было настроено

✅ **SvelteKit** - установлен и настроен  
✅ **Tailwind CSS v4** - установлен через `@tailwindcss/vite`  
✅ **TypeScript** - настроен  
✅ **Компоненты чата** - готовы к использованию  
✅ **API интеграция** - настроена для связи с бэкендом  
✅ **Современный UI** - с градиентами и темной темой  

## Структура компонентов

```
src/lib/components/
├── ChatContainer.svelte   # Главный контейнер с логикой
├── ChatMessage.svelte     # Отображение сообщения
└── ChatInput.svelte       # Поле ввода
```

## API

Endpoint: `POST /api/chat`

**Запрос:**
```json
{
  "message": "Привет!"
}
```

**Ответ:**
```json
{
  "message": "Привет! Чем могу помочь?",
  "sources": ["doc1.pdf", "doc2.txt"]
}
```

## Горячие клавиши

- `Enter` - отправить сообщение
- `Shift + Enter` - новая строка

## Следующие шаги

1. **Запустите бэкенд** на порту 8000
2. **Настройте CORS** на бэкенде для `http://localhost:5173`
3. **Адаптируйте API endpoint** в `src/routes/api/chat/+server.ts` под свой бэкенд

## Возможные проблемы

### Ошибка версии Node.js

```
npm error engine Unsupported engine
npm error notsup Required: {"node":"^20.19 || ^22.12 || >=24"}
```

**Решение:** Используйте `nvm use 22.12.0`

### Бэкенд не отвечает

Убедитесь, что:
1. Бэкенд запущен на правильном порту
2. CORS настроен правильно
3. URL в `.env` или `config.ts` корректен

## Деплой

```bash
# Сборка для production
npm run build

# Предпросмотр
npm run preview
```

Для деплоя используйте:
- **Vercel** (рекомендуется для SvelteKit)
- **Netlify**
- **Cloudflare Pages**

См. [SvelteKit Adapters](https://svelte.dev/docs/kit/adapters)