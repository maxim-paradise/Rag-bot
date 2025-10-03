"""
Тест полного RAG pipeline
"""
import os
import sys
import tempfile
from pathlib import Path

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot.rag_system import RAGSystem
from ml.rag_bot.document_loader import DocumentLoader

def create_test_documents():
    """Создаем тестовые документы"""
    test_docs = {
        "ai_basics.txt": """
        Искусственный интеллект (ИИ) - это область компьютерных наук, которая занимается созданием интеллектуальных машин.
        Машинное обучение - это подполе ИИ, которое позволяет компьютерам учиться без явного программирования.
        Глубокое обучение использует нейронные сети с множественными слоями для решения сложных задач.
        """,
        
        "python_programming.txt": """
        Python - это высокоуровневый язык программирования общего назначения.
        Python известен своей простотой и читаемостью кода.
        Популярные библиотеки Python включают NumPy, Pandas, TensorFlow и PyTorch.
        Django и Flask - это популярные веб-фреймворки для Python.
        """,
        
        "data_science.txt": """
        Наука о данных сочетает статистику, программирование и предметную экспертизу.
        Основные этапы работы с данными: сбор, очистка, анализ и визуализация.
        Pandas - библиотека для работы с данными в Python.
        Matplotlib и Seaborn используются для визуализации данных.
        """
    }
    
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp()
    
    for filename, content in test_docs.items():
        file_path = Path(temp_dir) / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    return temp_dir, list(test_docs.keys())

def test_full_pipeline():
    """Тест полного RAG pipeline"""
    print("🧪 Тестирование полного RAG pipeline...")
    
    try:
        # 1. Создаем тестовые документы
        print("\n📚 Создаем тестовые документы...")
        temp_dir, doc_names = create_test_documents()
        
        # 2. Инициализируем RAG систему
        print("\n🚀 Инициализируем RAG систему...")
        rag_system = RAGSystem(
            embeddings_model="cointegrated/rubert-tiny2",
            llm_provider="local",
            chunk_size=200,
            overlap=50
        )
        
        # 3. Загружаем документы
        print("\n📖 Загружаем документы...")
        file_paths = [str(Path(temp_dir) / name) for name in doc_names]
        load_result = rag_system.load_documents(file_paths)
        
        print(f"Результат загрузки: {load_result}")
        assert load_result["success"], "Загрузка документов не удалась"
        assert load_result["total_documents"] == 3, f"Ожидалось 3 документа, получено {load_result['total_documents']}"
        assert load_result["total_chunks"] > 0, "Не созданы чанки"
        
        # 4. Тестируем поиск
        print("\n🔍 Тестируем поиск...")
        search_results = rag_system.search("машинное обучение", top_k=3)
        assert len(search_results) > 0, "Поиск не дал результатов"
        
        print(f"Найдено {len(search_results)} результатов:")
        for i, result in enumerate(search_results):
            print(f"  {i+1}. Сходство: {result['similarity']:.3f}")
            print(f"     Файл: {result['metadata']['filename']}")
            print(f"     Текст: {result['document'][:100]}...")
        
        # 5. Тестируем RAG ответы
        print("\n❓ Тестируем RAG ответы...")
        
        test_questions = [
            "Что такое машинное обучение?",
            "Какие библиотеки Python популярны?",
            "Что такое наука о данных?",
            "Как называется язык программирования Python?"
        ]
        
        for question in test_questions:
            print(f"\nВопрос: {question}")
            response = rag_system.ask(question, top_k=3)
            
            print(f"Статус: {response['status']}")
            print(f"Источников: {response['sources_count']}")
            print(f"Ответ: {response['answer'][:200]}...")
            
            assert response["status"] in ["success", "no_results"], f"Неожиданный статус: {response['status']}"
            if response["status"] == "success":
                assert len(response["answer"]) > 0, "Пустой ответ"
                assert response["sources_count"] > 0, "Нет источников"
        
        # 6. Тестируем чат
        print("\n💬 Тестируем чат...")
        chat_response = rag_system.chat("Расскажи о Python")
        print(f"Тип ответа: {chat_response['type']}")
        print(f"Ответ: {chat_response['answer'][:200]}...")
        
        assert chat_response["status"] == "success", "Чат не работает"
        assert len(chat_response["answer"]) > 0, "Пустой ответ чата"
        
        # 7. Проверяем статус системы
        print("\n📊 Проверяем статус системы...")
        status = rag_system.get_status()
        print(f"Статус системы: {status['system_status']}")
        print(f"Документов в БД: {status['vector_store']['documents_count']}")
        print(f"LLM статус: {status['llm_service']['status']}")
        
        assert status["system_status"] == "ready", "Система не готова"
        
        print("\n✅ Все тесты полного pipeline прошли успешно!")
        
        # Очистка
        import shutil
        shutil.rmtree(temp_dir)
        print("🧹 Временные файлы удалены")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        
        # Очистка в случае ошибки
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass
        
        return False

def test_edge_cases():
    """Тест граничных случаев"""
    print("\n🧪 Тестирование граничных случаев...")
    
    try:
        rag_system = RAGSystem()
        
        # Тест с пустым вопросом
        response = rag_system.ask("")
        assert response["status"] in ["success", "no_results"], "Пустой вопрос должен обрабатываться"
        
        # Тест с вопросом без релевантных документов
        response = rag_system.ask("Как приготовить борщ?")
        assert response["status"] in ["success", "no_results"], "Неожиданный статус"
        
        # Тест поиска без результатов
        search_results = rag_system.search("несуществующая тема", top_k=5)
        assert isinstance(search_results, list), "Поиск должен возвращать список"
        
        print("✅ Граничные случаи обработаны корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в граничных случаях: {e}")
        return False

def test_performance():
    """Тест производительности"""
    print("\n⚡ Тестирование производительности...")
    
    try:
        import time
        
        rag_system = RAGSystem()
        
        # Тест времени поиска
        start_time = time.time()
        results = rag_system.search("искусственный интеллект", top_k=10)
        search_time = time.time() - start_time
        
        print(f"Время поиска: {search_time:.3f} сек")
        print(f"Найдено результатов: {len(results)}")
        
        # Тест времени генерации ответа
        start_time = time.time()
        response = rag_system.ask("Что такое ИИ?", top_k=3)
        answer_time = time.time() - start_time
        
        print(f"Время генерации ответа: {answer_time:.3f} сек")
        print(f"Статус ответа: {response['status']}")
        
        assert search_time < 5.0, f"Поиск слишком медленный: {search_time:.3f} сек"
        assert answer_time < 10.0, f"Генерация ответа слишком медленная: {answer_time:.3f} сек"
        
        print("✅ Производительность в норме")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тестах производительности: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск тестов полного RAG pipeline...")
    
    success_count = 0
    total_tests = 3
    
    # Основной тест pipeline
    if test_full_pipeline():
        success_count += 1
    
    # Тест граничных случаев
    if test_edge_cases():
        success_count += 1
    
    # Тест производительности
    if test_performance():
        success_count += 1
    
    print(f"\n📊 Результаты тестирования:")
    print(f"Пройдено тестов: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 Все тесты успешно пройдены!")
        print("✅ RAG система готова к использованию")
    else:
        print("⚠️ Некоторые тесты не пройдены")
        print("🔧 Требуется доработка")