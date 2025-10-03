# 🛠️ Команды для Управления Backend

## 📦 Установка

```bash
# Создание виртуального окружения и установка зависимостей
python -m venv venv; venv\Scripts\activate; pip install -r requirements-minimal.txt

# Или полная установка
python -m venv venv; venv\Scripts\activate; pip install -r requirements.txt
```

## 🚀 Запуск

```bash
# Активация окружения и запуск сервера
venv\Scripts\activate; python run.py

# Или запуск с тестированием
venv\Scripts\activate; python test_setup.py; python run.py
```

## 🧪 Тестирование

```bash
# Проверка установки
venv\Scripts\activate; python test_setup.py

# Тест API (после запуска сервера)
curl http://localhost:8000/health
```

## 📊 Полезные команды

```bash
# Проверка установленных пакетов
pip list

# Обновление pip
python -m pip install --upgrade pip

# Установка дополнительных пакетов
pip install jupyter notebook

# Очистка кэша pip
pip cache purge
```

## 🔧 Решение проблем

```bash
# Переустановка виртуального окружения
rmdir /s venv; python -m venv venv; venv\Scripts\activate; pip install -r requirements-minimal.txt

# Установка только CPU версии PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Проверка конфликтов зависимостей
pip check
```