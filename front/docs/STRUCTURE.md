# Структура проекта Frontend

## 📁 Обзор структуры

```
front/
├── src/
│   ├── lib/
│   │   ├── components/          # Компоненты UI
│   │   │   ├── Sidebar.svelte          # Боковая панель навигации
│   │   │   ├── Header.svelte           # Верхний заголовок
│   │   │   ├── ChatContainer.svelte    # Контейнер чата
│   │   │   ├── ChatMessage.svelte      # Отдельное сообщение
│   │   │   ├── ChatInput.svelte        # Поле ввода
│   │   │   ├── ChatList.svelte         # Список чатов
│   │   │   ├── ProjectList.svelte      # Список проектов
│   │   │   └── EmptyState.svelte       # Пустое состояние
│   │   ├── stores/              # Svelte stores для состояния
│   │   │   └── chat.ts                 # Store для чатов и проектов
│   │   ├── utils/               # Утилиты
│   │   │   └── date.ts                 # Функции работы с датами
│   │   ├── types.ts             # TypeScript типы
│   │   └── config.ts            # Конфигурация
│   ├── routes/
│   │   ├── api/
│   │   │   └── chat/
│   │   │       └── +server.ts          # API endpoint для чата
│   │   ├── +layout.svelte              # Главный layout
│   │   └── +page.svelte                # Главная страница
│   ├── app.css                  # Глобальные стили (Tailwind)
│   └── app.html                 # HTML template
├── static/                      # Статические файлы
├── package.json
├── svelte.config.js             # Конфигурация SvelteKit
├── vite.config.ts               # Конфигурация Vite
├── tsconfig.json                # Конфигурация TypeScript
├── README.md                    # Основная документация
├── SETUP.md                     # Инструкции по настройке
└── STRUCTURE.md                 # Этот файл
```

## 🎨 Архитектура компонентов

### Layout System

```
+layout.svelte (главный контейнер)
├── Sidebar (боковая панель)
│   ├── ProjectList (список проектов)
│   └── ChatList (список чатов)
├── Header (верхний заголовок)
└── +page.svelte (главная страница)
    ├── EmptyState (если нет активного чата)
    └── ChatContainer (если есть активный чат)
        ├── ChatMessage[] (список сообщений)
        └── ChatInput (поле ввода)
```

## 🔄 Управление состоянием

### Stores (`src/lib/stores/chat.ts`)

**Основные stores:**
- `chats` - список всех чатов
- `currentChatId` - ID текущего активного чата
- `projects` - список проектов
- `sidebarOpen` - состояние sidebar (открыт/закрыт)

**Функции:**
- `createNewChat(projectId?)` - создать новый чат
- `updateChatTitle(chatId, title)` - обновить название чата
- `addMessageToChat(chatId, message)` - добавить сообщение в чат
- `deleteChat(chatId)` - удалить чат
- `getChatsByProject(projectId)` - получить чаты проекта

## 🎯 Основные компоненты

### Sidebar.svelte
- Навигация по приложению
- GPTs секция (Explore, Code Copilot, Wolfram и т.д.)
- Список проектов
- Список чатов
- Профиль пользователя

### ChatContainer.svelte
- Управление сообщениями чата
- Отправка сообщений в API
- Автоматическая прокрутка
- Индикатор загрузки

### ChatMessage.svelte
- Отображение сообщения
- Аватар (пользователь/ассистент)
- Источники информации (для RAG)
- Timestamp

### ChatInput.svelte
- Поле ввода с автоматическим изменением размера
- Отправка по Enter
- Новая строка по Shift+Enter
- Кнопка отправки

### EmptyState.svelte
- Приветственное сообщение
- Карточки с предложениями
- Быстрые действия

## 🔌 API Integration

### Endpoint: `/api/chat`

**Файл:** `src/routes/api/chat/+server.ts`

**Request:**
```typescript
POST /api/chat
{
  "message": "User question here"
}
```

**Response:**
```typescript
{
  "message": "AI response",
  "sources": ["source1", "source2"]  // optional
}
```

**Настройка бэкенда:**
- По умолчанию: `http://localhost:8000`
- Через .env: `BACKEND_URL=http://your-backend:port`

## 🎨 Styling

### Tailwind CSS v4
- Используется через `@tailwindcss/vite` плагин
- Импорт в `app.css`: `@import 'tailwindcss';`
- Темная тема поддерживается через `dark:` префикс

### Цветовая схема
- **Sidebar**: slate-900 (темный)
- **Main**: white / slate-50 (светлый)
- **Акценты**: 
  - Blue-Purple градиент для AI
  - Emerald-Teal градиент для пользователя
  - Проекты: blue, green, yellow, purple

## 🚀 Best Practices

### 1. Компоненты
- Используем Svelte 5 runes (`$state`, `$props`, `$effect`, `$derived`)
- Props типизированы через интерфейс
- Компоненты переиспользуемые и изолированные

### 2. State Management
- Глобальное состояние в stores
- Локальное состояние через `$state`
- Derived state через `$derived`

### 3. TypeScript
- Все интерфейсы в `src/lib/types.ts`
- Строгая типизация props
- Type safety для API responses

### 4. Accessibility
- Все кнопки имеют `aria-label`
- Keyboard navigation поддерживается
- Semantic HTML используется

### 5. Performance
- Lazy loading для больших списков
- Оптимизированная прокрутка
- Минимальные re-renders

## 📱 Responsive Design

- **Desktop**: Sidebar всегда видим
- **Tablet**: Sidebar можно скрыть
- **Mobile**: Sidebar overlay (TODO)

## 🔐 Environment Variables

```env
BACKEND_URL=http://localhost:8000
PUBLIC_APP_NAME=AI Chatbot RAG
PUBLIC_APP_VERSION=1.0.0
```

## 🧪 Development Workflow

```bash
# 1. Переключить Node версию
nvm use 22.12.0

# 2. Установить зависимости
npm install

# 3. Запустить dev server
npm run dev

# 4. Открыть в браузере
http://localhost:5173
```

## 📦 Build & Deploy

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

## 🔮 Будущие улучшения

- [ ] Поиск по чатам
- [ ] Экспорт чатов
- [ ] Настройки пользователя
- [ ] Темы оформления
- [ ] Markdown рендеринг в сообщениях
- [ ] Code syntax highlighting
- [ ] Drag & drop файлов
- [ ] Voice input
- [ ] Multi-language support
- [ ] Offline mode

## 📚 Ресурсы

- [SvelteKit Docs](https://svelte.dev/docs/kit)
- [Svelte 5 Runes](https://svelte.dev/docs/svelte/what-are-runes)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript](https://www.typescriptlang.org)