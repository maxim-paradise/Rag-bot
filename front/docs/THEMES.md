# Система тем и стилей

## 🎨 Обзор

Проект использует глобальные CSS переменные с цветовой схемой в формате `oklch()` для поддержки светлой и темной темы, вдохновленной дизайном ChatGPT.

## 📁 Структура стилей

```
src/
├── styles/
│   └── global.css          # Глобальные стили и CSS переменные
├── app.css                 # Импорт глобальных стилей
└── components/             # Компоненты используют CSS переменные
```

## 🌓 Цветовая схема

### Светлая тема (по умолчанию)
- **Background**: Чистый белый/светло-серый
- **Foreground**: Темно-серый текст
- **Sidebar**: Светлый фон с тонкими границами
- **Primary**: Синий-фиолетовый градиент

### Темная тема (ChatGPT-style)
- **Background**: Очень темный серый (почти черный)
- **Foreground**: Светло-серый текст
- **Sidebar**: Почти черный фон
- **Primary**: Яркий синий-фиолетовый

## 🎯 CSS Переменные

### Основные цвета

```css
:root {
  --background           /* Основной фон */
  --foreground           /* Основной текст */
  --card                 /* Фон карточек */
  --primary              /* Акцентный цвет */
  --secondary            /* Вторичный цвет */
  --muted                /* Приглушенный фон */
  --muted-foreground     /* Приглушенный текст */
  --border               /* Цвет границ */
  --destructive          /* Цвет удаления/ошибок */
}
```

### Sidebar

```css
:root {
  --sidebar-background        /* Фон sidebar */
  --sidebar-foreground        /* Текст sidebar */
  --sidebar-accent            /* Hover состояние */
  --sidebar-border            /* Границы в sidebar */
}
```

### Специальные цвета

```css
:root {
  --user-gradient-from        /* Начало градиента пользователя */
  --user-gradient-to          /* Конец градиента пользователя */
  --ai-gradient-from          /* Начало градиента AI */
  --ai-gradient-to            /* Конец градиента AI */
  --message-ai-bg             /* Фон сообщения AI */
  --message-user-bg           /* Фон сообщения пользователя */
}
```

## 🛠️ Использование в компонентах

### Utility классы

```svelte
<!-- Фоны -->
<div class="bg-background">...</div>
<div class="bg-card">...</div>
<div class="bg-muted">...</div>

<!-- Текст -->
<p class="text-foreground">...</p>
<p class="text-muted-foreground">...</p>
<p class="text-primary">...</p>

<!-- Границы -->
<div class="border-border">...</div>
```

### Специальные классы

```svelte
<!-- Sidebar -->
<aside class="sidebar">
  <button class="sidebar-item">Item</button>
  <button class="sidebar-item active">Active Item</button>
</aside>

<!-- Сообщения -->
<div class="message-ai">AI response</div>
<div class="message-user">User message</div>

<!-- Аватары -->
<div class="avatar-ai">AI</div>
<div class="avatar-user">User</div>

<!-- Кнопки -->
<button class="btn-primary">Primary Button</button>

<!-- Поля ввода -->
<input class="input-field" />
```

## 🌙 Переключение темы

### Автоматическое определение

По умолчанию тема определяется системными настройками:

```css
/* Автоматически применится при темной теме ОС */
.dark { ... }
```

### Ручное переключение

Добавьте класс `.dark` к корневому элементу:

```javascript
// Включить темную тему
document.documentElement.classList.add('dark');

// Включить светлую тему
document.documentElement.classList.remove('dark');

// Переключить
document.documentElement.classList.toggle('dark');
```

### Компонент переключателя (пример)

```svelte
<script>
  import { browser } from '$app/environment';
  
  let isDark = $state(false);
  
  $effect(() => {
    if (browser) {
      isDark = document.documentElement.classList.contains('dark');
    }
  });
  
  function toggleTheme() {
    if (browser) {
      document.documentElement.classList.toggle('dark');
      isDark = !isDark;
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }
  }
</script>

<button onclick={toggleTheme}>
  {isDark ? '🌞' : '🌙'}
</button>
```

## 📐 Размеры и скругления

```css
--radius: 0.75rem;      /* Стандартное скругление */
--radius-sm: 0.5rem;    /* Маленькое скругление */
--radius-lg: 1rem;      /* Большое скругление */
```

## 🎭 Анимации

### Встроенные анимации

```svelte
<!-- Плавное появление -->
<div class="animate-fade-in">...</div>

<!-- Выезжание сбоку -->
<div class="animate-slide-in">...</div>
```

### Transition (Svelte)

```svelte
<script>
  import { slide, fade } from 'svelte/transition';
</script>

<div transition:fade>...</div>
<div transition:slide>...</div>
```

## 📱 Адаптивность

Все компоненты адаптивны благодаря Tailwind CSS:

```svelte
<!-- Mobile-first подход -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  ...
</div>
```

## 🔧 Кастомизация

### Изменение цветов

Отредактируйте `src/styles/global.css`:

```css
:root {
  --primary: oklch(0.60 0.25 270);  /* Ваш цвет */
}

.dark {
  --primary: oklch(0.65 0.28 270);  /* Для темной темы */
}
```

### Добавление новых переменных

```css
:root {
  --custom-color: oklch(0.5 0.2 180);
}

.dark {
  --custom-color: oklch(0.6 0.25 180);
}
```

Использование:

```svelte
<div style="background: oklch(var(--custom-color))">...</div>
```

## 🎨 Генератор oklch цветов

Используйте онлайн инструменты:
- https://oklch.com/
- https://colorjs.io/apps/picker/

## 💡 Best Practices

1. **Всегда используйте CSS переменные** вместо хардкода цветов
2. **Тестируйте в обеих темах** перед коммитом
3. **Используйте semantic названия** классов (.sidebar-item вместо .blue-button)
4. **Следуйте контрастности** для доступности (WCAG AA)
5. **oklch() формат** для более точной работы с цветом

## 🐛 Отладка

### Проверка текущей темы

```javascript
console.log(document.documentElement.classList.contains('dark'));
```

### Просмотр CSS переменных

```javascript
getComputedStyle(document.documentElement).getPropertyValue('--primary');
```

### Dev Tools

В Chrome/Firefox DevTools:
1. Inspect element
2. Computed tab
3. Filter по `--` для просмотра переменных

## 📚 Ресурсы

- [oklch colors](https://oklch.com/)
- [Tailwind CSS](https://tailwindcss.com)
- [CSS Color 4](https://www.w3.org/TR/css-color-4/)
- [ChatGPT Design Reference](https://chat.openai.com)