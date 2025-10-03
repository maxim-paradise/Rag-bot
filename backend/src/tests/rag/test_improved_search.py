import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import EmbeddingsService, VectorStore

print("🚀 Тестируем улучшенный поиск с русской моделью...")

# Создаем сервисы с русской моделью
embeddings = EmbeddingsService()  # Теперь использует русскую модель
vector_store = VectorStore(db_path="./data/test_vector_db_ru")

print("✅ Сервисы созданы")

# Тестовые документы
documents = [
    "Собака лает на улице",
    "Кот спит на диване", 
    "Птица поет в саду"
]

# Создаем embeddings
print("📊 Создаем embeddings...")
doc_embeddings = embeddings.encode_batch(documents)

# Метаданные с более детальной информацией
metadata = [
    {"type": "animal", "action": "barking", "sound": True, "activity": "active"},
    {"type": "animal", "action": "sleeping", "sound": False, "activity": "passive"},
    {"type": "bird", "action": "singing", "sound": True, "activity": "active"}
]

# Добавляем в векторную БД
print("💾 Добавляем документы в векторную БД...")
doc_ids = vector_store.add_documents(documents, doc_embeddings, metadata)
print(f"✅ Добавлено документов: {len(doc_ids)}")

# Тестируем поиск
print("🔍 Тестируем поиск...")
query = "Животное издает звуки"
query_embedding = embeddings.encode(query)

results = vector_store.search(query_embedding, top_k=3)

print(f"🎯 Запрос: '{query}'")
print("📋 Результаты поиска:")
for i, result in enumerate(results, 1):
    print(f"  {i}. Документ: {result['document']}")
    print(f"     Похожесть: {result['similarity']:.3f}")
    print(f"     Метаданные: {result['metadata']}")
    print()

print("🎉 Тест с русской моделью завершен!")