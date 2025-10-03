# AI Chatbot RAG - Frontend

Фронтенд приложение для AI чатбота с поддержкой RAG (Retrieval-Augmented Generation), построенное на SvelteKit и Tailwind CSS.

## 🚀 Технологии

- **SvelteKit** - Full-stack фреймворк для Svelte
- **Tailwind CSS v4** - Utility-first CSS фреймворк
- **TypeScript** - Типизация
- **Vite** - Сборщик и dev сервер

## 📦 Установка

```bash
# Убедитесь, что используете Node.js 20.19+ или 22.12+
nvm use 22.12.0

# Установка зависимостей
npm install
```

## 🛠️ Разработка

```bash
# Запуск dev сервера
npm run dev

# Запуск с автоматическим открытием браузера
npm run dev -- --open
```

Приложение будет доступно по адресу: http://localhost:5173

## 🏗️ Сборка

```bash
# Сборка продакшн версии
npm run build

# Предпросмотр продакшн сборки
npm run preview
```

## ⚙️ Конфигурация

### Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```env
BACKEND_URL=http://localhost:8000
PUBLIC_APP_NAME=AI Chatbot RAG
PUBLIC_APP_VERSION=1.0.0
```

### Подключение к бэкенду

По умолчанию фронтенд ожидает, что бэкенд запущен на `http://localhost:8000`.

Для изменения адреса бэкенда:
1. Измените переменную `BACKEND_URL` в файле `.env`
2. Или измените `BACKEND_URL` в файле `src/routes/api/chat/+server.ts`

## 📁 Структура проекта

```
src/
├── lib/
│   ├── components/
│   │   ├── ChatContainer.svelte  # Основной контейнер чата
│   │   ├── ChatMessage.svelte    # Компонент сообщения
│   │   └── ChatInput.svelte      # Поле ввода сообщений
│   └── types.ts                  # TypeScript типы
├── routes/
│   ├── api/
│   │   └── chat/
│   │       └── +server.ts        # API endpoint для чата
│   ├── +layout.svelte            # Главный layout
│   └── +page.svelte              # Главная страница
└── app.css                       # Глобальные стили (Tailwind)
```

## 🎨 Особенности UI

- ✨ Современный градиентный дизайн
- 🌓 Поддержка темной темы
- 📱 Адаптивная верстка
- ⌨️ Удобные горячие клавиши (Enter для отправки, Shift+Enter для новой строки)
- 🔄 Анимации загрузки
- 📄 Отображение источников информации (RAG)

## 🔧 Интеграция с бэкендом

API endpoint ожидает следующий формат запроса:

```typescript
POST /api/chat
{
  "message": "Ваш вопрос"
}
```

Ожидаемый формат ответа:

```typescript
{
  "message": "Ответ ассистента",
  "sources": ["источник1", "источник2"]  // опционально
}
```

## 📝 Дальнейшая настройка

### Добавление новых компонентов

```bash
# Компоненты размещаются в src/lib/components/
touch src/lib/components/YourComponent.svelte
```

### Добавление новых страниц

```bash
# Страницы размещаются в src/routes/
mkdir src/routes/your-page
touch src/routes/your-page/+page.svelte
```

### Настройка Tailwind CSS

Tailwind v4 использует новый подход с `@import 'tailwindcss'` в `app.css`.

Для кастомизации добавьте CSS переменные или используйте стандартные утилиты Tailwind.

## 🐛 Отладка

```bash
# Проверка типов
npm run check

# Проверка типов в режиме watch
npm run check:watch
```

## 📚 Дополнительные ресурсы

- [SvelteKit Documentation](https://svelte.dev/docs/kit)
- [Svelte Documentation](https://svelte.dev/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🤝 Разработка

Проект использует:
- **Svelte 5** с новым синтаксисом runes (`$state`, `$props`, `$effect`)
- **TypeScript** для типобезопасности
- **Tailwind CSS v4** для стилизации