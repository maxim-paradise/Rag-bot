// API для чата - можно заменить на реальный endpoint
export interface ChatRequest {
  message: string;
  model?: string;
  temperature?: number;
  max_tokens?: number;
}

export interface ChatResponse {
  response: string;
  model: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

// Мок-ответы для демонстрации
const mockResponses = [
  "Это отличный вопрос! Я AI-ассистент и готов помочь вам с различными задачами. Что именно вас интересует?",
  "Понимаю ваш запрос. Могу предоставить подробную информацию по этой теме. Давайте разберем это пошагово.",
  "Интересный вопрос! Позвольте мне объяснить это подробнее. Есть несколько важных аспектов, которые стоит рассмотреть.",
  "Спасибо за вопрос! Это важная тема, и я готов поделиться своими знаниями. Вот что я могу рассказать...",
  "Отлично! Давайте разберем это подробно. Я постараюсь дать вам максимально полезный и точный ответ.",
  "Понимаю, что вас интересует эта тема. Позвольте мне предоставить вам структурированный и понятный ответ.",
  "Это важный вопрос, который требует детального рассмотрения. Вот мой анализ ситуации...",
  "Спасибо за обращение! Я готов помочь вам разобраться в этом вопросе. Начнем с основ...",
];

export const chatAPI = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    // Имитируем задержку API
    await new Promise((resolve) =>
      setTimeout(resolve, 1000 + Math.random() * 2000)
    );

    // Выбираем случайный ответ
    const response =
      mockResponses[Math.floor(Math.random() * mockResponses.length)];

    return {
      response: `${response}\n\nВаш вопрос: "${request.message}"`,
      model: request.model || "gpt-3.5-turbo",
      usage: {
        prompt_tokens: Math.floor(request.message.length / 4),
        completion_tokens: Math.floor(response.length / 4),
        total_tokens: Math.floor(
          (request.message.length + response.length) / 4
        ),
      },
    };
  },
};

// Для интеграции с реальным API (например, OpenAI)
export const openAIAPI = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: request.model || "gpt-3.5-turbo",
        messages: [
          {
            role: "user",
            content: request.message,
          },
        ],
        temperature: request.temperature || 0.7,
        max_tokens: request.max_tokens || 1000,
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const data = await response.json();

    return {
      response: data.choices[0].message.content,
      model: data.model,
      usage: data.usage,
    };
  },
};
