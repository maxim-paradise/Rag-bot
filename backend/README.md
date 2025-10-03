# ML/AI Backend Platform

Комплексная платформа для изучения машинного обучения и искусственного интеллекта с поддержкой RAG чатбота и ML экспериментов.

## 🚀 Возможности

### RAG Чатбот
- Загрузка и обработка документов
- Векторный поиск с ChromaDB
- Генерация ответов с контекстом
- Память диалогов

### ML Эксперименты
- **Text Classification** - классификация текстов
- **Sentiment Analysis** - анализ тональности
- **Text Generation** - генерация текста
- **Question Answering** - ответы на вопросы
- **Computer Vision** - компьютерное зрение

### Поддерживаемые Библиотеки
- 🤗 **Transformers** - предобученные модели
- 🔥 **PyTorch** - глубокое обучение
- 🧠 **TensorFlow** - машинное обучение
- 📊 **Scikit-learn** - классические ML алгоритмы
- 👁️ **OpenCV** - компьютерное зрение
- 📈 **Weights & Biases** - отслеживание экспериментов

## 📁 Структура Проекта

```
backend/
├── src/
│   ├── main.py                    # FastAPI приложение
│   ├── config/
│   │   └── settings.py           # Конфигурация
│   ├── models/
│   │   └── experiment.py         # Модели данных
│   ├── services/
│   │   └── ml_experiment_service.py  # ML сервисы
│   └── api/
│       ├── ml_experiments.py     # ML API
│       ├── visualization.py      # Визуализация
│       ├── chat.py              # RAG чатбот
│       ├── documents.py         # Документы
│       └── models.py            # Управление моделями
├── data/
│   ├── experiments/             # Эксперименты
│   ├── models/                  # Сохраненные модели
│   ├── datasets/               # Датасеты
│   └── visualizations/         # Графики
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Установка

1. **Клонируйте репозиторий:**
```bash
cd ai_chatbot_rag/backend
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\\Scripts\\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте окружение:**
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими API ключами
```

5. **Запустите сервер:**
```bash
cd src
python main.py
```

## 🎯 Быстрый Старт

### 1. Создание ML Эксперимента

```python
import requests

# Создать эксперимент
response = requests.post("http://localhost:8000/api/ml/experiments", json={
    "name": "Мой первый эксперимент",
    "type": "sentiment_analysis",
    "description": "Анализ тональности отзывов"
})

experiment_id = response.json()["id"]
```

### 2. Быстрое Демо

```python
# Запустить быстрое демо
demo_response = requests.post("http://localhost:8000/api/ml/experiments/quick-demo", json={
    "task": "sentiment-analysis",
    "texts": ["Я люблю этот продукт!", "Ужасное качество"]
})

print(demo_response.json())
```

### 3. Визуализация Результатов

```python
# Получить графики эксперимента
viz_response = requests.get(f"http://localhost:8000/api/visualization/experiments/{experiment_id}/charts")
charts = viz_response.json()["charts"]
```

## 📊 API Endpoints

### ML Эксперименты
- `POST /api/ml/experiments` - Создать эксперимент
- `GET /api/ml/experiments` - Список экспериментов
- `GET /api/ml/experiments/{id}` - Получить эксперимент
- `POST /api/ml/experiments/{id}/train` - Запустить обучение
- `POST /api/ml/experiments/quick-demo` - Быстрое демо

### Визуализация
- `GET /api/visualization/experiments/{id}/charts` - Графики эксперимента
- `GET /api/visualization/charts/{chart_id}` - Получить график
- `POST /api/visualization/custom-visualization` - Создать график

### Модели
- `GET /api/models/` - Список моделей
- `POST /api/models/upload` - Загрузить модель
- `POST /api/models/{id}/inference` - Запустить инференс

## 🧪 Примеры Экспериментов

### Text Classification
```python
training_data = [
    {"text": "Отличный продукт!", "label": 1},
    {"text": "Плохое качество", "label": 0}
]

requests.post(f"http://localhost:8000/api/ml/experiments/{experiment_id}/train", json={
    "model_name": "distilbert-base-uncased",
    "train_data": training_data,
    "num_labels": 2
})
```

### Sentiment Analysis
```python
requests.post("http://localhost:8000/api/ml/experiments/quick-demo", json={
    "task": "sentiment-analysis",
    "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "texts": ["Я счастлив!", "Мне грустно"]
})
```

### Text Generation
```python
requests.post("http://localhost:8000/api/ml/experiments/quick-demo", json={
    "task": "text-generation",
    "model": "gpt2",
    "prompts": ["Искусственный интеллект это"],
    "max_length": 100
})
```

## 🔧 Конфигурация

Основные настройки в `.env`:

```env
# API
API_HOST=0.0.0.0
API_PORT=8000

# ML Settings
DEVICE=auto  # auto, cpu, cuda, mps
DEFAULT_BATCH_SIZE=32
DEFAULT_LEARNING_RATE=0.001

# External APIs
OPENAI_API_KEY=your_key
HF_TOKEN=your_token
WANDB_API_KEY=your_key
```

## 📈 Мониторинг

Интеграция с Weights & Biases для отслеживания экспериментов:
- Метрики обучения
- Визуализация потерь
- Сравнение экспериментов
- Сохранение артефактов

## 🎓 Обучающие Материалы

Рекомендуемый порядок изучения:

1. **Основы NLP** - токенизация, embeddings
2. **Transformers** - BERT, GPT, T5
3. **Fine-tuning** - дообучение моделей
4. **RAG Systems** - поиск + генерация
5. **Computer Vision** - CNN, Vision Transformers
6. **MLOps** - эксперименты, деплой

## 🤝 Интеграция с Frontend

API готово для интеграции с Vue.js frontend:
- CORS настроен для localhost:3000, localhost:5173
- REST API с JSON responses
- Статические файлы для визуализаций
- WebSocket поддержка (планируется)

## 📝 Лицензия

MIT License - используйте свободно для обучения и экспериментов!