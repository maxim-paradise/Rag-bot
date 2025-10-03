// Конфигурация приложения
export const config = {
  // URL бэкенда (можно переопределить через переменные окружения)
  backendUrl: import.meta.env.BACKEND_URL || "http://localhost:8000",

  // Публичные переменные
  appName: import.meta.env.PUBLIC_APP_NAME || "AI Chatbot RAG",
  appVersion: import.meta.env.PUBLIC_APP_VERSION || "1.0.0",

  // API endpoints
  api: {
    chat: "/api/chat",
  },
} as const;
