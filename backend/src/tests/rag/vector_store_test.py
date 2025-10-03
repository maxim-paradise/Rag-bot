import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import EmbeddingsService, VectorStore

print("🧪 Тестируем VectorStore...")

# Создаем сервисы
embeddings = EmbeddingsService()
vector_store = VectorStore(db_path="./data/test_vector_db")

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

# Метаданные
metadata = [
    {"type": "animal", "action": "barking"},
    {"type": "animal", "action": "sleeping"},
    {"type": "bird", "action": "singing"}
]

# Добавляем в векторную БД
print("💾 Добавляем документы в векторную БД...")
doc_ids = vector_store.add_documents(documents, doc_embeddings, metadata)
print(f"✅ Добавлено документов: {len(doc_ids)}")

# Информация о коллекции
info = vector_store.get_collection_info()
print(f"📊 Информация о БД: {info}")

# Тестируем поиск
print("🔍 Тестируем поиск...")
query = "Животное издает звуки"
query_embedding = embeddings.encode(query)

results = vector_store.search(query_embedding, top_k=2)

print(f"🎯 Запрос: '{query}'")
print("📋 Результаты поиска:")
for i, result in enumerate(results, 1):
    print(f"  {i}. Документ: {result['document']}")
    print(f"     Похожесть: {result['similarity']:.3f}")
    print(f"     Метаданные: {result['metadata']}")
    print()

print("🎉 Тест VectorStore завершен!")