"""
Embeddings Service - создание векторных представлений
"""
from typing import List
# sentence-transformers — это популярная библиотека для создания эмбеддингов (векторных представлений) текстов с помощью предобученных моделей на базе BERT, RoBERTa и других трансформеров.
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingsService:
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2"):
        self.model_name = model_name
        print(f"Загружаем модель: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Модель embeddings загружена")
    
    def encode(self, text: str) -> List[float]:
       embeddings = self.model.encode(text)
       return embeddings.tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    def similarity(self, text1: str, text2: str) -> float:
      emb1 = self.encode(text1)
      emb2 = self.encode(text2)
      
      dot_product = np.dot(emb1, emb2)
      norm1 = np.linalg.norm(emb1)
      norm2 = np.linalg.norm(emb2)

      return dot_product / (norm1 * norm2)
