import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import LLMService, ChatMessage

print("🤖 Тестируем LLM Service...")

# Тестируем разные провайдеры
providers = [
    ("openai", "gpt-3.5-turbo"),
    ("anthropic", "claude-3-haiku-20240307"),
    ("local", "microsoft/DialoGPT-medium")
]

for provider, model in providers:
    print(f"\n📋 Тестируем провайдер: {provider}")
    
    try:
        llm = LLMService(provider=provider, model=model)
        
        # Получаем статус
        status = llm.get_status()
        print(f"✅ Статус: {status}")
        
        # Тестируем простой чат
        print("💬 Тестируем простой чат...")
        messages = [
            ChatMessage(role="system", content="Ты дружелюбный помощник."),
            ChatMessage(role="user", content="Привет! Как дела?")
        ]
        
        response = llm.generate_chat_response(messages)
        print(f"🤖 Ответ: {response[:100]}...")
        
        # Тестируем RAG
        print("📚 Тестируем RAG...")
        question = "Что такое машинное обучение?"
        context = """Машинное обучение — это область искусственного интеллекта, 
        которая изучает алгоритмы и статистические модели, которые компьютерные системы 
        используют для эффективного выполнения конкретной задачи без использования явных инструкций."""
        sources = [{"filename": "ml_guide.txt", "similarity": 0.9}]
        
        rag_response = llm.generate_rag_response(question, context, sources)
        print(f"📖 RAG ответ: {rag_response[:100]}...")
        
    except Exception as e:
        print(f"❌ Ошибка с провайдером {provider}: {e}")

print("\n🎉 Тест LLM Service завершен!")
print("\n📝 Заметки:")
print("- Для OpenAI установите: pip install openai")
print("- Для Anthropic установите: pip install anthropic") 
print("- Для локальных моделей установите: pip install transformers torch")
print("- Настройте переменные окружения OPENAI_API_KEY или ANTHROPIC_API_KEY")
print("- Без API ключей система работает в режиме заглушки")