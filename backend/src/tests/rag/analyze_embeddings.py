import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import EmbeddingsService

print("🔍 Анализируем embeddings для понимания поиска...")

embeddings = EmbeddingsService()

# Тестовые фразы
query = "Животное издает звуки"
doc1 = "Собака лает на улице"  # Правильный ответ
doc2 = "Кот спит на диване"    # Неправильный ответ
doc3 = "Птица поет в саду"     # Тоже правильный

print(f"🎯 Запрос: '{query}'")
print()

# Считаем similarity для каждого документа
docs = [doc1, doc2, doc3]
similarities = []

for doc in docs:
    sim = embeddings.similarity(query, doc)
    similarities.append(sim)
    print(f"📄 '{doc}' -> similarity: {sim:.3f}")

print()
print("🧠 Анализ:")
print("1. Модель all-MiniLM-L6-v2 обучена на английском языке")
print("2. Русские фразы переводятся в векторы через английские токены")
print("3. 'Животное' и 'кот' могут быть близки в векторном пространстве")
print("4. 'издает звуки' и 'спит' - разные действия, но модель может их путать")

print()
print("💡 Решения:")
print("1. Использовать русскую модель: 'cointegrated/rubert-tiny2'")
print("2. Улучшить метаданные и фильтрацию")
print("3. Настроить threshold для similarity")
print("4. Использовать более точную модель embeddings")