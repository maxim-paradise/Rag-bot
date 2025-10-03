import sys
import os
from pathlib import Path

# Добавляем путь к src для нормальных импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.rag_bot import DocumentLoader, Document

print("📄 Тестируем DocumentLoader...")

# Создаем загрузчик
loader = DocumentLoader()

# Создаем тестовые файлы
test_dir = Path("./data/test_documents")
test_dir.mkdir(parents=True, exist_ok=True)

# 1. Создаем тестовый TXT файл
txt_file = test_dir / "test.txt"
with open(txt_file, 'w', encoding='utf-8') as f:
    f.write("Это тестовый документ.\nВторая строка текста.\nТретья строка с русским текстом.")

print("✅ Создан тестовый TXT файл")

# 2. Создаем тестовый MD файл
md_file = test_dir / "test.md"
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# Заголовок\n\nЭто **markdown** документ с *форматированием*.\n\n## Подзаголовок\n\nСписок:\n- Пункт 1\n- Пункт 2")

print("✅ Создан тестовый MD файл")

# 3. Создаем тестовый Python файл
py_file = test_dir / "test.py"
with open(py_file, 'w', encoding='utf-8') as f:
    f.write('def hello():\n    """Тестовая функция"""\n    print("Привет, мир!")\n\nif __name__ == "__main__":\n    hello()')

print("✅ Создан тестовый PY файл")

print("\n🔍 Тестируем загрузку отдельных файлов...")

# Тестируем загрузку TXT файла
try:
    doc_txt = loader.load_file(str(txt_file))
    print(f"📄 TXT файл загружен:")
    print(f"   Размер контента: {len(doc_txt.content)} символов")
    print(f"   Имя файла: {doc_txt.metadata['filename']}")
    print(f"   Расширение: {doc_txt.metadata['file_extension']}")
    print(f"   Первые 50 символов: {doc_txt.content[:50]}...")
except Exception as e:
    print(f"❌ Ошибка загрузки TXT: {e}")

# Тестируем загрузку MD файла
try:
    doc_md = loader.load_file(str(md_file))
    print(f"📄 MD файл загружен:")
    print(f"   Размер контента: {len(doc_md.content)} символов")
    print(f"   Имя файла: {doc_md.metadata['filename']}")
    print(f"   Первые 50 символов: {doc_md.content[:50]}...")
except Exception as e:
    print(f"❌ Ошибка загрузки MD: {e}")

# Тестируем загрузку PY файла
try:
    doc_py = loader.load_file(str(py_file))
    print(f"📄 PY файл загружен:")
    print(f"   Размер контента: {len(doc_py.content)} символов")
    print(f"   Имя файла: {doc_py.metadata['filename']}")
    print(f"   Первые 50 символов: {doc_py.content[:50]}...")
except Exception as e:
    print(f"❌ Ошибка загрузки PY: {e}")

print("\n📁 Тестируем загрузку директории...")

# Тестируем загрузку всей директории
try:
    documents = loader.load_directory(str(test_dir))
    print(f"📁 Загружено документов из директории: {len(documents)}")
    
    for i, doc in enumerate(documents, 1):
        print(f"   {i}. {doc.metadata['filename']} ({doc.metadata['file_extension']}) - {len(doc.content)} символов")
        
except Exception as e:
    print(f"❌ Ошибка загрузки директории: {e}")

print("\n🌐 Тестируем загрузку URL (опционально)...")

# Тестируем загрузку URL (если есть интернет)
try:
    # Простая страница для теста
    url_doc = loader.load_url("https://httpbin.org/html")
    print(f"🌐 URL загружен:")
    print(f"   Заголовок: {url_doc.metadata.get('title', 'Нет заголовка')}")
    print(f"   Размер контента: {len(url_doc.content)} символов")
    print(f"   Первые 100 символов: {url_doc.content[:100]}...")
except ImportError as e:
    print(f"⚠️ Для загрузки URL нужны дополнительные библиотеки: {e}")
except Exception as e:
    print(f"⚠️ Ошибка загрузки URL (возможно, нет интернета): {e}")

print("\n❌ Тестируем обработку ошибок...")

# Тестируем несуществующий файл
try:
    loader.load_file("несуществующий_файл.txt")
except FileNotFoundError as e:
    print(f"✅ Правильно обработана ошибка: {e}")

# Тестируем несуществующую директорию
try:
    loader.load_directory("несуществующая_директория")
except ValueError as e:
    print(f"✅ Правильно обработана ошибка: {e}")

print("\n🎉 Тест DocumentLoader завершен!")
print("\n📚 Что умеет DocumentLoader:")
print("✅ Загружать текстовые файлы (TXT, MD, PY, JS, HTML, CSS)")
print("✅ Загружать PDF файлы (требует PyPDF2)")
print("✅ Загружать DOCX файлы (требует python-docx)")
print("✅ Загружать веб-страницы (требует requests, beautifulsoup4)")
print("✅ Загружать целые директории с фильтрацией")
print("✅ Извлекать метаданные файлов")
print("✅ Обрабатывать различные кодировки")
print("✅ Обрабатывать ошибки")