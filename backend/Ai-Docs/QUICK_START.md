# 🚀 Быстрый Старт - ML/AI Backend Platform

## 📋 Что создано

Вы получили полноценную платформу для изучения машинного обучения:

### ✅ Готовая архитектура
- **FastAPI backend** с ML экспериментами
- **Система визуализации** результатов
- **RAG чатбот** (базовая структура)
- **API для frontend** интеграции

### ✅ Поддерживаемые технологии
- 🤗 **Transformers** - BERT, GPT, T5
- 🔥 **PyTorch** - глубокое обучение
- 🧠 **TensorFlow** - ML алгоритмы
- 📊 **Scikit-learn** - классические методы
- 👁️ **OpenCV** - компьютерное зрение

---

## 🛠️ Установка и Запуск

### 1. Перейдите в папку backend
```bash
cd ai_chatbot_rag/backend
```

### 2. Создайте виртуальное окружение
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установите зависимости

**⚠️ Если возникают проблемы с установкой, используйте минимальную версию:**

```bash
# Быстрая установка (рекомендуется)
pip install -r requirements-minimal.txt

# Или полная установка (если нужны все возможности)
pip install -r requirements.txt
```

**💡 Подробные инструкции по установке смотрите в `install_instructions.md`**

### 4. Настройте окружение (опционально)
```bash
# Скопируйте пример конфигурации
copy .env.example .env

# Отредактируйте .env файл:
# - Добавьте OpenAI API ключ для LLM
# - Добавьте Hugging Face токен для моделей
# - Добавьте Weights & Biases ключ для трекинга
```

### 5. Запустите сервер
```bash
# Простой запуск
python run.py

# Или через uvicorn
cd src
python main.py
```

### 6. Откройте браузер
- **API Документация**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/

---

## 🎯 Первые Шаги

### 1. Создайте свой первый ML эксперимент

**Откройте новый терминал и выполните:**

```bash
# Установите requests для тестирования API
pip install requests
```

**Создайте файл `test_experiment.py`:**

```python
import requests
import json

# Создать эксперимент
response = requests.post("http://localhost:8000/api/ml/experiments", json={
    "name": "Мой первый эксперимент",
    "type": "sentiment_analysis",
    "description": "Тестирование анализа тональности"
})

print("Эксперимент создан:", response.json())
experiment_id = response.json()["id"]

# Запустить быстрое демо
demo_response = requests.post("http://localhost:8000/api/ml/experiments/quick-demo", json={
    "task": "sentiment-analysis",
    "texts": [
        "Я очень доволен этим продуктом!",
        "Ужасное качество, не рекомендую",
        "Нормальный товар, ничего особенного"
    ]
})

print("\nРезультаты анализа тональности:")
print(json.dumps(demo_response.json(), indent=2, ensure_ascii=False))
```

**Запустите тест:**
```bash
python test_experiment.py
```

### 2. Посмотрите доступные модели

```python
import requests

models = requests.get("http://localhost:8000/api/ml/models/available")
print("Доступные модели:", models.json())
```

### 3. Создайте визуализацию

```python
import requests

# Создать кастомную визуализацию
viz_data = {
    "type": "bar",
    "title": "Мой первый график",
    "data": [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
        {"category": "C", "value": 15}
    ],
    "x_column": "category",
    "y_column": "value"
}

viz_response = requests.post("http://localhost:8000/api/visualization/custom-visualization", json=viz_data)
print("Визуализация создана:", viz_response.json())
```

---

## 📚 Что дальше?

### 🎓 Следуйте плану обучения
Откройте файл `ML_LEARNING_PLAN.md` - там детальный план на 20 недель изучения ML.

### 🔗 Интегрируйте с frontend
Ваш backend готов для интеграции с Vue.js frontend. API endpoints настроены с CORS.

### 📊 Экспериментируйте
- Загружайте свои датасеты
- Тренируйте модели
- Создавайте визуализации
- Отслеживайте эксперименты

### 🤝 Расширяйте функциональность
- Добавьте новые типы экспериментов
- Интегрируйте другие ML библиотеки
- Создайте кастомные визуализации
- Добавьте новые API endpoints

---

## 🆘 Помощь и Поддержка

### Частые проблемы

**1. Ошибка импорта библиотек**
```bash
# Убедитесь, что виртуальное окружение активировано
pip install -r requirements.txt
```

**2. Порт уже занят**
```bash
# Измените порт в src/main.py или в переменной API_PORT
```

**3. Нет GPU для PyTorch**
```bash
# Установите CPU версию PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Логи и отладка
- Логи сервера выводятся в консоль
- Ошибки API возвращаются в JSON формате
- Используйте `/health` endpoint для проверки статуса

---

## 🎉 Поздравляем!

Вы создали мощную платформу для изучения ML/AI! 

**Ваши возможности:**
- ✅ Экспериментировать с современными ML моделями
- ✅ Визуализировать результаты
- ✅ Отслеживать прогресс обучения
- ✅ Интегрировать с frontend
- ✅ Масштабировать для production

**Удачи в изучении Machine Learning! 🚀**