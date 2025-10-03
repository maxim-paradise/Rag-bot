# 🚀 Инструкции по Установке

## Проблема с зависимостями? Вот решение!

### 📦 Вариант 1: Минимальная установка (рекомендуется для начала)

```bash
# Активируйте виртуальное окружение
cd ai_chatbot_rag/backend
python -m venv venv
venv\Scripts\activate  # Windows

# Установите минимальные зависимости
pip install -r requirements-minimal.txt

# Запустите сервер
python run.py
```

### 📦 Вариант 2: Пошаговая установка

```bash
# 1. Основные зависимости
pip install fastapi uvicorn python-multipart pydantic python-dotenv

# 2. ML библиотеки (выберите одну из опций)

# Опция A: Только CPU (быстрее, меньше места)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentence-transformers

# Опция B: С поддержкой GPU (если есть NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers sentence-transformers

# 3. Дополнительные библиотеки (по желанию)
pip install numpy pandas scikit-learn matplotlib plotly requests openai
```

### 📦 Вариант 3: Полная установка (если нужны все возможности)

```bash
# Обновите pip
python -m pip install --upgrade pip

# Установите все зависимости
pip install -r requirements.txt
```

## 🔧 Решение частых проблем

### Проблема: "Could not find a version that satisfies the requirement"

**Решение:**
```bash
# Обновите pip
python -m pip install --upgrade pip

# Используйте минимальные требования
pip install -r requirements-minimal.txt
```

### Проблема: "No module named 'uvicorn'"

**Решение:**
```bash
# Убедитесь, что виртуальное окружение активировано
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Установите uvicorn
pip install uvicorn fastapi
```

### Проблема: Медленная установка PyTorch

**Решение:**
```bash
# Установите CPU версию (быстрее)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## ✅ Проверка установки

```bash
# Запустите сервер
python run.py

# Если видите это сообщение - все работает:
# 🚀 Starting ML/AI Backend Platform...
# 📊 Dashboard: http://localhost:8000/docs
```

## 🎯 Быстрый тест

```python
# Создайте файл test.py
import requests

response = requests.get("http://localhost:8000/health")
print("Статус:", response.json())
```

## 💡 Советы

1. **Начните с минимальной установки** - потом добавите нужные библиотеки
2. **Используйте виртуальное окружение** - избежите конфликтов
3. **Обновите pip** - решит большинство проблем с зависимостями
4. **CPU версия PyTorch** - достаточно для изучения

**Если проблемы остались - напишите, помогу! 🤝**