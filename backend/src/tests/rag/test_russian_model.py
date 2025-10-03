import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import EmbeddingsService

print("🇷🇺 Тестируем русскую модель embeddings...")

# Создаем сервис с русской моделью
embeddings_ru = EmbeddingsService(model_name="cointegrated/rubert-tiny2")

query = "Животное издает звуки"
doc1 = "Собака лает на улице"
doc2 = "Кот спит на диване" 
doc3 = "Птица поет в саду"

print(f"🎯 Запрос: '{query}'")
print()

docs = [doc1, doc2, doc3]
for doc in docs:
    sim = embeddings_ru.similarity(query, doc)
    print(f"📄 '{doc}' -> similarity: {sim:.3f}")

print()
print("✅ Русская модель должна давать более точные результаты!")