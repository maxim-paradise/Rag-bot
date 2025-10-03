import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import VectorStore

print("🔍 Инспектируем ChromaDB...")

# Подключаемся к существующей БД
vector_store = VectorStore(db_path="./data/test_vector_db")

# Получаем информацию о коллекции
info = vector_store.get_collection_info()
print(f"📊 Информация о коллекции: {info}")

# Получаем все данные из коллекции
all_data = vector_store.collection.get()

print(f"\n📋 Всего документов: {len(all_data['ids']) if all_data['ids'] else 0}")

if all_data['ids']:
    print("\n📄 Документы в базе:")
    for i, doc_id in enumerate(all_data['ids']):
        print(f"  {i+1}. ID: {doc_id}")
        print(f"     Документ: {all_data['documents'][i]}")
        print(f"     Метаданные: {all_data['metadatas'][i]}")
        print(f"     Embedding (первые 5 значений): {all_data['embeddings'][i][:5] if all_data['embeddings'] else 'Нет'}")
        print()

print("🎉 Инспекция завершена!")