"""
Sentiment Analysis API endpoints
Здесь вы будете писать код для анализа тональности
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from pathlib import Path

router = APIRouter()

# Модели данных для API
class SentimentRequest(BaseModel):
    text: str
    
class BatchSentimentRequest(BaseModel):
    texts: List[str]
    
class SentimentResponse(BaseModel):
    text: str
    sentiment: str  # "positive", "negative", "neutral"
    confidence: float
    
class TrainRequest(BaseModel):
    texts: List[str]
    labels: List[str]  # ["positive", "negative", "neutral"]
    model_name: str = "sentiment_model"

# Импортируем ваш класс
try:
    from ml_projects.sentiment_analysis import SentimentAnalyzer
    # Создаем глобальный экземпляр анализатора
    analyzer = SentimentAnalyzer()
    ANALYZER_AVAILABLE = True
except Exception as e:
    print(f"Ошибка загрузки анализатора: {e}")
    analyzer = None
    ANALYZER_AVAILABLE = False

@router.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Анализ тональности одного текста - использует вашу модель
    """
    try:
        if not ANALYZER_AVAILABLE:
            raise HTTPException(status_code=500, detail="Анализатор не загружен")
        
        # Используем ваш анализатор
        result = analyzer.predict(request.text)
        
        return SentimentResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")

@router.post("/analyze-batch")
async def analyze_batch_sentiment(request: BatchSentimentRequest):
    """
    Анализ тональности нескольких текстов - использует вашу модель
    """
    try:
        if not ANALYZER_AVAILABLE:
            raise HTTPException(status_code=500, detail="Анализатор не загружен")
        
        # Используем ваш batch метод
        results = analyzer.predict_batch(request.texts)
        
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка batch анализа: {str(e)}")

@router.post("/train")
async def train_sentiment_model(request: TrainRequest):
    """
    Обучение модели на ваших данных
    
    TODO: Реализуйте обучение модели
    """
    try:
        # TODO: Добавьте валидацию данных
        if len(request.texts) != len(request.labels):
            raise HTTPException(status_code=400, detail="Количество текстов и меток должно совпадать")
        
        # TODO: Используйте ваш метод обучения
        # analyzer.train(request.texts, request.labels)
        
        return {
            "message": "Модель обучена успешно",
            "model_name": request.model_name,
            "samples_count": len(request.texts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")

@router.get("/models")
async def list_sentiment_models():
    """
    Список доступных моделей
    
    TODO: Реализуйте получение списка ваших моделей
    """
    # TODO: Сканируйте папку с моделями и верните список
    models_dir = Path("data/models/sentiment")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    models = []
    # TODO: Добавьте код для поиска ваших сохраненных моделей
    
    return {"models": models}

@router.get("/demo")
async def sentiment_demo():
    """
    Демо с примерами для тестирования - использует вашу модель
    """
    demo_texts = [
        "Я очень доволен этим продуктом!",
        "Ужасное качество, не рекомендую",
        "Обычный товар, ничего особенного",
        "Лучшая покупка в моей жизни!",
        "Полное разочарование и потеря денег"
    ]
    
    if not ANALYZER_AVAILABLE:
        return {
            "error": "Анализатор не загружен",
            "demo_results": []
        }
    
    results = analyzer.predict_batch(demo_texts)
    
    return {
        "demo_results": results,
        "note": "Результаты получены с помощью вашей модели!"
    }