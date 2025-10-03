import sys
import os
import requests
import json
from pathlib import Path

print("🌐 Тестируем RAG API...")

# URL нашего API
BASE_URL = "http://127.0.0.1:8000/api/rag"

def test_health():
    """Тест проверки здоровья системы"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check прошел успешно:")
            print(f"   Статус: {data.get('status')}")
            print(f"   Документов в БД: {data.get('documents_count', 0)}")
            print(f"   Модель embeddings: {data.get('embeddings_model')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка health check: {e}")
        return False

def test_upload_document():
    """Тест загрузки документа"""
    try:
        # Создаем тестовый файл
        test_content = """Это тестовый документ для RAG системы.
        
Содержание документа:
- Информация о машинном обучении
- Примеры использования векторного поиска
- Тестовые данные для проверки работы системы

Машинное обучение - это область искусственного интеллекта, которая изучает алгоритмы и статистические модели."""
        
        test_file_path = Path("./data/test_rag_document.txt")
        test_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Загружаем файл через API
        with open(test_file_path, 'rb') as f:
            files = {'files': ('test_document.txt', f, 'text/plain')}
            response = requests.post(f"{BASE_URL}/documents/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Документ загружен успешно:")
            print(f"   Сообщение: {data.get('message')}")
            print(f"   Результаты: {len(data.get('results', []))}")
            return True
        else:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка теста загрузки: {e}")
        return False

def test_search():
    """Тест поиска документов"""
    try:
        search_data = {
            "query": "машинное обучение",
            "top_k": 3
        }
        
        response = requests.post(
            f"{BASE_URL}/search",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            results = response.json()
            print("✅ Поиск выполнен успешно:")
            print(f"   Найдено результатов: {len(results)}")
            
            for i, result in enumerate(results, 1):
                print(f"   {i}. Similarity: {result.get('similarity', 0):.3f}")
                print(f"      Документ: {result.get('document', '')[:100]}...")
                print()
            return True
        else:
            print(f"❌ Ошибка поиска: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка теста поиска: {e}")
        return False

def test_chat():
    """Тест чата с документами"""
    try:
        chat_data = {
            "question": "Что такое машинное обучение?",
            "top_k": 2
        }
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Чат работает успешно:")
            print(f"   Вопрос: {data.get('question')}")
            print(f"   Ответ: {data.get('answer', '')[:200]}...")
            print(f"   Источников: {len(data.get('sources', []))}")
            return True
        else:
            print(f"❌ Ошибка чата: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка теста чата: {e}")
        return False

def test_list_documents():
    """Тест получения списка документов"""
    try:
        response = requests.get(f"{BASE_URL}/documents/list")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Список документов получен:")
            print(f"   Всего документов: {data.get('total_documents', 0)}")
            
            documents = data.get('documents', [])
            for i, doc in enumerate(documents[:3], 1):  # Показываем первые 3
                print(f"   {i}. {doc.get('filename')} ({doc.get('content_length')} символов)")
            return True
        else:
            print(f"❌ Ошибка получения списка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка теста списка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов RAG API...")
    print("📝 Убедитесь, что сервер запущен: python src/main.py")
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Upload Document", test_upload_document),
        ("Search Documents", test_search),
        ("Chat with Documents", test_chat),
        ("List Documents", test_list_documents)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 Тест: {test_name}")
        if test_func():
            passed += 1
        print("-" * 50)
    
    print(f"🎉 Результаты: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("✅ Все тесты прошли! RAG API работает корректно")
    else:
        print("⚠️ Некоторые тесты не прошли. Проверьте сервер и зависимости")

if __name__ == "__main__":
    main()