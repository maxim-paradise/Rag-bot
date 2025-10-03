import sys
import os

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import EmbeddingsService

print("🧪 Тестируем Embeddings Service...")

embeddings = EmbeddingsService()

vec1 = embeddings.encode("Собака лает")
print(f"✅ Вектор 1: длина {len(vec1)}")

vec2 = embeddings.encode("Пес гавкает")
print(f"✅ Вектор 2: длина {len(vec2)}")

similarity = embeddings.similarity("Собака лает", "Пес гавкает")
print(f"✅ Похожесть: {similarity:.3f}")

print("🎉 Тест завершен!")