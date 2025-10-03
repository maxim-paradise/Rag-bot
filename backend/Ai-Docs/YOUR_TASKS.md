# 🎯 Ваши Задачи по ML Проектам

## 📋 Проект 1: Анализ Тональности (Sentiment Analysis)

### 🎯 Цель
Создать систему, которая определяет эмоциональную окраску текста: положительная, отрицательная или нейтральная.

### 📁 Файлы для работы
- **`src/ml_projects/sentiment_analysis.py`** - Основной код проекта (ваш класс SentimentAnalyzer)
- **`src/api/sentiment_analysis.py`** - API endpoints (уже готовы, нужно подключить ваш класс)
- **`data/sentiment_examples.json`** - Примеры данных для обучения

### ✅ Задача 1: Реализовать SentimentAnalyzer

**Откройте файл `src/ml_projects/sentiment_analysis.py`**

#### Вариант 1: Простой (рекомендуется для начала)
```python
# В методе __init__:
from transformers import pipeline
self.model = pipeline("sentiment-analysis", 
                     model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# В методе predict:
result = self.model(text)[0]
return {
    "text": text,
    "sentiment": self._map_label(result["label"]),
    "confidence": result["score"]
}
```

#### Вариант 2: Классические методы ML
```python
# В методе __init__:
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
self.vectorizer = TfidfVectorizer()
self.model = LogisticRegression()

# В методе train:
X = self.vectorizer.fit_transform(texts)
self.model.fit(X, labels)
```

### ✅ Задача 2: Тестирование

1. **Запустите сервер**: `python run.py`
2. **Откройте**: http://localhost:8000/docs
3. **Найдите раздел**: "Sentiment Analysis"
4. **Протестируйте endpoints**:
   - `/api/sentiment/demo` - демо примеры
   - `/api/sentiment/analyze` - анализ одного текста

### ✅ Задача 3: Обучение на своих данных

1. **Загрузите данные** из `data/sentiment_examples.json`
2. **Реализуйте метод `train`** в вашем классе
3. **Протестируйте** через `/api/sentiment/train`

### 🎯 Критерии успеха
- [ ] Класс SentimentAnalyzer создан и работает
- [ ] API endpoints возвращают реальные результаты
- [ ] Модель правильно определяет тональность простых фраз
- [ ] Обучение на новых данных работает

---

## 📋 Проект 2: Классификация Текста (следующий)

### 🎯 Цель
Автоматически определять категорию текста (например: спорт, технологии, политика).

### 📁 Файлы (создам после завершения Проекта 1)
- `src/ml_projects/text_classification.py`
- `src/api/text_classification.py`

---

## 📋 Проект 3: Генерация Текста (продвинутый)

### 🎯 Цель
Создавать новый текст на основе промпта (как ChatGPT, но проще).

---

## 🛠️ Полезные команды

### Установка дополнительных библиотек
```bash
# Для Transformers
pip install torch transformers

# Для классических методов
pip install scikit-learn

# Для работы с данными
pip install pandas numpy
```

### Тестирование API
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Тест анализа тональности
curl -X POST "http://localhost:8000/api/sentiment/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "Отличный продукт!"}'
```

---

## 📚 Ресурсы для изучения

### Документация
- [Transformers](https://huggingface.co/docs/transformers) - готовые модели
- [Scikit-learn](https://scikit-learn.org/) - классические методы
- [FastAPI](https://fastapi.tiangolo.com/) - для API

### Модели для анализа тональности
- `cardiffnlp/twitter-roberta-base-sentiment-latest` - хорошая модель
- `distilbert-base-uncased-finetuned-sst-2-english` - быстрая модель

---

## 🎯 Следующие шаги

1. **Начните с Проекта 1** - анализ тональности
2. **Реализуйте простой вариант** с готовой моделью
3. **Протестируйте через API**
4. **Улучшите** - добавьте обучение на своих данных
5. **Переходите к Проекту 2** - классификация текста

**Удачи! Пишите, если нужна помощь! 🚀**