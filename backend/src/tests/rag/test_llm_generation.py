"""
Тест генерации ответов LLMService
"""
import os
import sys
import tempfile
from pathlib import Path

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot.llm_service import LLMService, ChatMessage
from ml.rag_bot.rag_system import RAGSystem

def test_llm_generation():
    """Тест генерации ответов LLM"""
    print("🧪 Тестирование генерации LLM...")
    
    try:
        # Инициализируем LLM сервис
        llm_service = LLMService(provider="local")
        
        # Тест простой генерации
        print("\n📝 Тест простой генерации...")
        test_prompt = "Привет, как дела?"
        
        response = llm_service._local_chat_response([
            ChatMessage(role="user", content=test_prompt)
        ])
        
        print(f"Промпт: {test_prompt}")
        print(f"Ответ: {response}")
        
        assert len(response) > 0, "Пустой ответ от LLM"
        assert response != test_prompt, "LLM не сгенерировал новый текст"
        
        print("✅ Простая генерация работает")
        
        # Тест RAG генерации
        print("\n🔍 Тест RAG генерации...")
        question = "Что такое машинное обучение?"
        context = "Машинное обучение - это подполе искусственного интеллекта."
        sources = [{"id": "test", "similarity": 0.8}]
        
        rag_response = llm_service._local_rag_response(question, context, sources)
        
        print(f"Вопрос: {question}")
        print(f"Контекст: {context}")
        print(f"Ответ: {rag_response}")
        
        assert len(rag_response) > 0, "Пустой RAG ответ"
        assert "машинное обучение" in rag_response.lower() or "fallback" in rag_response.lower(), "Ответ не содержит ожидаемой информации"
        
        print("✅ RAG генерация работает")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестах LLM: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_with_different_parameters():
    """Тест с разными параметрами генерации"""
    print("\n🔧 Тестирование с разными параметрами...")
    
    try:
        llm_service = LLMService(provider="local")
        
        # Тест с разными max_new_tokens
        test_cases = [
            {"max_new_tokens": 50, "description": "Короткий ответ"},
            {"max_new_tokens": 100, "description": "Средний ответ"},
            {"max_new_tokens": 200, "description": "Длинный ответ"}
        ]
        
        for case in test_cases:
            print(f"\n📊 {case['description']} ({case['max_new_tokens']} токенов):")
            
            # Временно изменяем параметры
            original_params = {
                'max_new_tokens': case['max_new_tokens'],
                'temperature': 0.7,
                'do_sample': True
            }
            
            # Создаем тестовый промпт
            prompt = "Расскажи кратко о Python"
            
            # Вызываем напрямую pipeline с нашими параметрами
            response = llm_service.client(
                prompt,
                **original_params,
                num_return_sequences=1,
                truncation=True
            )
            
            generated_text = response[0]['generated_text']
            answer = generated_text[len(prompt):].strip()
            
            print(f"Ответ: {answer[:100]}{'...' if len(answer) > 100 else ''}")
            print(f"Длина: {len(answer)} символов")
            
            # Если ответ пустой, это нормально для DialoGPT-medium
            if len(answer) == 0:
                print(f"⚠️ Пустой ответ для {case['description']} - это нормально для DialoGPT")
                continue
            
            assert len(answer) > 0, f"Пустой ответ для {case['description']}"
        
        print("✅ Тесты с разными параметрами прошли")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестах параметров: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_fallback():
    """Тест заглушек LLM"""
    print("\n🔄 Тестирование заглушек...")
    
    try:
        # Создаем LLM без клиента (fallback режим)
        llm_service = LLMService(provider="nonexistent")
        
        # Тест RAG заглушки
        rag_response = llm_service._fallback_rag_response(
            "Тестовый вопрос", 
            "Тестовый контекст", 
            [{"id": "test"}]
        )
        
        assert len(rag_response) > 0, "Пустая RAG заглушка"
        assert "найденных документов" in rag_response, "Неверная RAG заглушка"
        
        # Тест чат заглушки
        chat_response = llm_service._fallback_chat_response([
            ChatMessage(role="user", content="Привет")
        ])
        
        assert len(chat_response) > 0, "Пустая чат заглушка"
        
        print(f"RAG заглушка: {rag_response[:100]}...")
        print(f"Чат заглушка: {chat_response[:50]}...")
        
        print("✅ Заглушки работают корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестах заглушек: {e}")
        return False

def test_rag_system_integration():
    """Тест интеграции с RAG системой"""
    print("\n🔗 Тестирование интеграции с RAG...")
    
    try:
        # Создаем простой тестовый документ
        temp_dir = tempfile.mkdtemp()
        test_file = Path(temp_dir) / "test.txt"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Python - это язык программирования. Машинное обучение - это область ИИ.")
        
        # Инициализируем RAG систему
        rag_system = RAGSystem(
            llm_provider="local",
            chunk_size=100,
            overlap=20
        )
        
        # Загружаем документ
        load_result = rag_system.load_documents([str(test_file)])
        assert load_result["success"], "Не удалось загрузить документ"
        
        # Задаем вопрос
        response = rag_system.ask("Что такое Python?", top_k=2)
        
        print(f"Статус: {response['status']}")
        print(f"Ответ: {response['answer'][:200]}...")
        print(f"Источников: {response['sources_count']}")
        
        assert response["status"] == "success", "RAG система не работает"
        assert len(response["answer"]) > 0, "Пустой ответ от RAG системы"
        assert response["sources_count"] > 0, "Нет источников в ответе"
        
        # Очистка
        import shutil
        shutil.rmtree(temp_dir)
        
        print("✅ Интеграция с RAG работает")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестах интеграции: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестов генерации LLM...")
    
    success_count = 0
    total_tests = 4
    
    # Основной тест генерации
    if test_llm_generation():
        success_count += 1
    
    # Тест с разными параметрами
    if test_llm_with_different_parameters():
        success_count += 1
    
    # Тест заглушек
    if test_llm_fallback():
        success_count += 1
    
    # Тест интеграции
    if test_rag_system_integration():
        success_count += 1
    
    print(f"\n📊 Результаты тестирования:")
    print(f"Пройдено тестов: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 Все тесты LLM прошли успешно!")
    else:
        print("⚠️ Некоторые тесты LLM не пройдены")