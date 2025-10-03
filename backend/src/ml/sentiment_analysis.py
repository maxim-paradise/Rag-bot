"""
Sentiment Analysis Project
Ваш первый ML проект - анализ тональности текста

ЗАДАЧА:
Создать систему, которая определяет эмоциональную окраску текста:
- Положительная (positive)
- Отрицательная (negative) 
- Нейтральная (neutral)

ПОДХОДЫ (выберите один или попробуйте несколько):
1. Использовать готовую модель из Transformers
2. Обучить свою модель на датасете
3. Использовать классические ML методы (TF-IDF + классификатор)
"""

from typing import Dict, List, Any, Optional
import json
from pathlib import Path

class SentimentAnalyzer:
    """
    Ваш класс для анализа тональности
    
    TODO: Реализуйте этот класс
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Инициализация анализатора
        
        TODO: Ваши задачи:
        1. Загрузить или создать модель
        2. Настроить токенизатор (если нужен)
        3. Подготовить все необходимое для работы
        
        Варианты реализации:
        - Использовать transformers.pipeline("sentiment-analysis")
        - Загрузить предобученную модель BERT/RoBERTa
        - Создать свою модель с sklearn
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        
        # TODO: Раскомментируйте и реализуйте нужный подход
        
        # Подход 1: Готовая модель из Transformers
        # from transformers import pipeline
        # self.model = pipeline("sentiment-analysis", 
        #                      model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        
        # Подход 2: Кастомная модель
        # self._load_custom_model()
        
        # Подход 3: Классические методы
        # self._init_classical_model()

        # Используем настоящую ML модель
        try:
            from transformers import pipeline
            self.model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            print("Загружена модель DistilBERT для анализа тональности")
        except ImportError:
            print("Transformers не установлен. Установите: pip install transformers torch")
            self.model = None
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            self.model = None
        
        print("SentimentAnalyzer инициализирован")
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Предсказание тональности для одного текста
        
        Args:
            text: Текст для анализа
            
        Returns:
            Dict с полями: sentiment, confidence, text
            
        TODO: Реализуйте этот метод
        """
        
        # TODO: Ваш код здесь
        # Примеры реализации:
        
        # Подход 1: Transformers
        # result = self.model(text)[0]
        # return {
        #     "text": text,
        #     "sentiment": self._map_label(result["label"]),
        #     "confidence": result["score"]
        # }
        
        # Подход 2: Кастомная модель
        # processed_text = self._preprocess(text)
        # prediction = self.model.predict([processed_text])
        # confidence = self.model.predict_proba([processed_text]).max()
        # return {
        #     "text": text,
        #     "sentiment": self._map_prediction(prediction[0]),
        #     "confidence": confidence
        # }
        
        # Используем настоящую ML модель
        if self.model is None:
            return {
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": "Модель не загружена. Установите transformers: pip install transformers torch"
            }
        
        try:
            # Получаем предсказание от модели
            result = self.model(text)[0]
            
            # Отладочная информация
            print(f"Анализ текста: '{text}'")
            print(f"Модель вернула: {result}")
            
            # Маппинг результата
            sentiment = self._map_label(result["label"])
            confidence = result["score"]
            
            print(f"Финальный результат: {sentiment} ({confidence})")
            print("-" * 50)
            
        except Exception as e:
            print(f"Ошибка при анализе: {e}")
            return {
                "text": text,
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }
        
        return {
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Предсказание для нескольких текстов
        
        TODO: Реализуйте batch обработку для ускорения
        """
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        return results
    
    def train(self, texts: List[str], labels: List[str], **kwargs):
        """
        Обучение модели на ваших данных
        
        Args:
            texts: Список текстов для обучения
            labels: Список меток ("positive", "negative", "neutral")
            
        TODO: Реализуйте обучение модели
        """
        
        # TODO: Ваш код обучения
        # Примеры подходов:
        
        # Подход 1: Fine-tuning BERT
        # from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
        # # Подготовка данных, создание датасета, обучение
        
        # Подход 2: Классические методы
        # from sklearn.feature_extraction.text import TfidfVectorizer
        # from sklearn.linear_model import LogisticRegression
        # self.vectorizer = TfidfVectorizer(max_features=10000)
        # X = self.vectorizer.fit_transform(texts)
        # self.model = LogisticRegression()
        # self.model.fit(X, labels)
        
        print(f"Обучение на {len(texts)} примерах завершено")
    
    def save_model(self, path: str):
        """
        Сохранение обученной модели
        
        TODO: Реализуйте сохранение вашей модели
        """
        model_dir = Path(path)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # TODO: Сохраните вашу модель
        # Примеры:
        # self.model.save_pretrained(path)  # для Transformers
        # joblib.dump(self.model, path / "model.pkl")  # для sklearn
        
        print(f"Модель сохранена в {path}")
    
    def load_model(self, path: str):
        """
        Загрузка сохраненной модели
        
        TODO: Реализуйте загрузку модели
        """
        # TODO: Загрузите вашу модель
        print(f"Модель загружена из {path}")
    
    def _preprocess(self, text: str) -> str:
        """
        Предобработка текста
        
        TODO: Добавьте нужную предобработку:
        - Очистка от HTML тегов
        - Нормализация регистра
        - Удаление лишних символов
        - Лемматизация (если нужна)
        """
        # Базовая очистка
        text = text.strip().lower()
        return text
    
    def _map_label(self, label: str) -> str:
        """
        Маппинг меток модели к вашему формату
        """
        # Для distilbert-base-uncased-finetuned-sst-2-english модели:
        mapping = {
            "NEGATIVE": "negative",
            "POSITIVE": "positive",
            # Для других моделей:
            "LABEL_0": "negative", 
            "LABEL_1": "positive"
        }
        
        return mapping.get(label, "neutral")

# TODO: Дополнительные утилиты для работы с данными

def load_dataset(file_path: str) -> tuple[List[str], List[str]]:
    """
    Загрузка датасета для обучения
    
    TODO: Реализуйте загрузку ваших данных
    Форматы: CSV, JSON, TXT
    """
    texts = []
    labels = []
    
    # TODO: Ваш код загрузки данных
    
    return texts, labels

def evaluate_model(analyzer: SentimentAnalyzer, test_texts: List[str], test_labels: List[str]) -> Dict[str, float]:
    """
    Оценка качества модели
    
    TODO: Реализуйте метрики качества:
    - Accuracy
    - Precision, Recall, F1-score
    - Confusion Matrix
    """
    predictions = []
    for text in test_texts:
        result = analyzer.predict(text)
        predictions.append(result["sentiment"])
    
    # TODO: Вычислите метрики
    # from sklearn.metrics import accuracy_score, classification_report
    
    return {
        "accuracy": 0.0,
        "f1_score": 0.0
    }

# TODO: Примеры использования (раскомментируйте после реализации)

# if __name__ == "__main__":
#     # Создание анализатора
#     analyzer = SentimentAnalyzer()
#     
#     # Тест на примерах
#     test_texts = [
#         "Я очень доволен покупкой!",
#         "Ужасный товар, не рекомендую",
#         "Обычный продукт, ничего особенного"
#     ]
#     
#     for text in test_texts:
#         result = analyzer.predict(text)
#         print(f"Текст: {text}")
#         print(f"Тональность: {result['sentiment']} ({result['confidence']:.2f})")
#         print("-" * 50)