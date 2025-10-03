/**
 * RAG API Service - для работы с RAG системой
 */

// Типы для RAG API
export interface Document {
  id: string;
  filename: string;
  content_length: number;
  file_extension: string;
  content_preview?: string;
}

export interface SearchResult {
  document: string;
  similarity: number;
  metadata: Record<string, any>;
  id: string;
}

export interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: SearchResult[];
}

export interface SimpleChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface LLMProvider {
  name: string;
  models: string[];
  requires_api_key: boolean;
  description: string;
}

export interface LLMConfig {
  provider: string;
  model: string;
  api_key?: string;
}

export interface UploadResult {
  filename: string;
  doc_id?: string;
  content_length?: number;
  status: "success" | "error";
  error?: string;
}

// Получаем URL бэкенда из переменных окружения
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
const RAG_API_BASE = `${BACKEND_URL}/api/rag`;

class RagApiService {
  /**
   * Проверка здоровья RAG системы
   */
  async healthCheck() {
    const response = await fetch(`${RAG_API_BASE}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return await response.json();
  }

  /**
   * Загрузка документов
   */
  async uploadDocuments(
    files: File[]
  ): Promise<{ message: string; results: UploadResult[] }> {
    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    const response = await fetch(`${RAG_API_BASE}/documents/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Поиск документов
   */
  async searchDocuments(
    query: string,
    topK: number = 5
  ): Promise<SearchResult[]> {
    const response = await fetch(`${RAG_API_BASE}/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`Search failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Чат с документами
   */
  async chatWithDocuments(question: string, topK: number = 3) {
    const response = await fetch(`${RAG_API_BASE}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`Chat failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Получить список документов
   */
  async getDocuments(): Promise<{
    total_documents: number;
    documents: Document[];
  }> {
    const response = await fetch(`${RAG_API_BASE}/documents/list`);

    if (!response.ok) {
      throw new Error(`Failed to get documents: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Удалить документ
   */
  async deleteDocument(docId: string): Promise<{ message: string }> {
    const response = await fetch(`${RAG_API_BASE}/documents/${docId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Delete failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Простой чат с AI (без документов)
   */
  async simpleChat(message: string, history: SimpleChatMessage[] = []) {
    const response = await fetch(`${RAG_API_BASE}/simple-chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        history: history.map((msg) => ({
          role: msg.role,
          content: msg.content,
        })),
      }),
    });

    if (!response.ok) {
      throw new Error(`Simple chat failed: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Получить статус LLM сервиса
   */
  async getLLMStatus() {
    const response = await fetch(`${RAG_API_BASE}/llm-status`);

    if (!response.ok) {
      throw new Error(`Failed to get LLM status: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Получить список доступных LLM провайдеров
   */
  async getLLMProviders(): Promise<{ providers: Record<string, LLMProvider> }> {
    const response = await fetch(`${RAG_API_BASE}/llm-providers`);

    if (!response.ok) {
      throw new Error(`Failed to get LLM providers: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Настроить LLM провайдер
   */
  async configureLLM(config: LLMConfig) {
    const response = await fetch(`${RAG_API_BASE}/configure-llm`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    });

    if (!response.ok) {
      throw new Error(`Failed to configure LLM: ${response.statusText}`);
    }

    return await response.json();
  }
}

export const ragApi = new RagApiService();
