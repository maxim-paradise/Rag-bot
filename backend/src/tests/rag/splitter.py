import tempfile
import os
from pathlib import Path

# Импортируем наш TextSplitter
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'rag_bot'))

from text_splitter import TextSplitter

def test_text_splitter_basic():
    """Тест базовой функциональности TextSplitter"""
    splitter = TextSplitter(chunk_size=100, overlap=20)
    
    # Тест с коротким текстом
    short_text = "Это короткий текст."
    chunks = splitter.split_text(short_text)
    assert len(chunks) == 1
    assert chunks[0] == short_text
    
    # Тест с пустым текстом
    empty_chunks = splitter.split_text("")
    assert empty_chunks == []
    
    # Тест с None
    none_chunks = splitter.split_text(None)
    assert none_chunks == []

def test_text_splitter_long_text():
    """Тест разбиения длинного текста"""
    splitter = TextSplitter(chunk_size=200, overlap=50)
    
    long_text = """
    Машинное обучение - это подраздел искусственного интеллекта, который фокусируется на использовании данных и алгоритмов для имитации способа обучения людей, постепенно улучшая свою точность. 
    Глубокое обучение - это подполе машинного обучения, основанное на искусственных нейронных сетях с множеством слоев. 
    Обработка естественного языка (NLP) - это область искусственного интеллекта, которая помогает компьютерам понимать, интерпретировать и манипулировать человеческим языком.
    """
    
    chunks = splitter.split_text(long_text)
    
    # Проверяем, что текст разбился на несколько чанков
    assert len(chunks) > 1
    
    # Проверяем, что каждый чанк не превышает лимит
    for chunk in chunks:
        assert len(chunk) <= splitter.chunk_size + 100  # Небольшой запас
    
    # Проверяем, что весь текст сохранился
    combined_text = " ".join(chunks)
    assert "машинное обучение" in combined_text.lower()
    assert "глубокое обучение" in combined_text.lower()

def test_text_splitter_overlap():
    """Тест перекрытия между чанками"""
    splitter = TextSplitter(chunk_size=150, overlap=30)
    
    text = """
    Первое предложение содержит важную информацию о машинном обучении.
    Второе предложение продолжает тему и добавляет детали.
    Третье предложение завершает мысль и подводит итоги.
    Четвертое предложение начинает новую тему о глубоком обучении.
    Пятое предложение развивает тему нейронных сетей.
    """
    
    chunks = splitter.split_text(text)
    
    # Проверяем перекрытие между соседними чанками
    if len(chunks) > 1:
        for i in range(1, len(chunks)):
            prev_chunk = chunks[i-1]
            current_chunk = chunks[i]
            
            # Проверяем, что есть общие слова
            prev_words = set(prev_chunk.lower().split())
            current_words = set(current_chunk.lower().split())
            common_words = prev_words.intersection(current_words)
            
            # Должно быть некоторое перекрытие
            assert len(common_words) > 0, f"Нет перекрытия между чанками {i-1} и {i}"

def test_text_splitter_sentence_boundaries():
    """Тест разбиения по границам предложений"""
    splitter = TextSplitter(chunk_size=100, overlap=20)
    
    text = "Первое предложение. Второе предложение! Третье предложение? Четвертое предложение."
    chunks = splitter.split_text(text)
    
    # Проверяем, что предложения не разрываются посередине
    for chunk in chunks:
        # Каждый чанк должен заканчиваться знаком препинания
        assert chunk.endswith(('.', '!', '?')), f"Чанк не заканчивается знаком препинания: {chunk}"

def test_text_splitter_clean_text():
    """Тест очистки текста"""
    splitter = TextSplitter()
    
    messy_text = "Текст   с    множественными    пробелами.\n\nИ с переносами строк."
    chunks = splitter.split_text(messy_text)
    
    # Проверяем, что лишние пробелы удалены
    for chunk in chunks:
        assert "   " not in chunk, "В чанке остались множественные пробелы"
        assert "\n\n" not in chunk, "В чанке остались множественные переносы"

def test_text_splitter_unicode():
    """Тест обработки Unicode символов"""
    splitter = TextSplitter(chunk_size=100, overlap=20)
    
    unicode_text = "Текст с русскими символами: привет мир! 🚀 Машинное обучение — это круто. Émojis and accents are supported too."
    chunks = splitter.split_text(unicode_text)
    
    # Проверяем, что Unicode символы сохранились
    combined_text = " ".join(chunks)
    assert "🚀" in combined_text
    assert "привет мир" in combined_text
    assert "Émojis" in combined_text

def test_text_splitter_edge_cases():
    """Тест граничных случаев"""
    splitter = TextSplitter(chunk_size=50, overlap=10)
    
    # Очень длинное предложение
    long_sentence = "Это очень длинное предложение " * 20 + "которое превышает размер чанка."
    chunks = splitter.split_text(long_sentence)
    
    # Должен разбиться на несколько чанков
    assert len(chunks) > 1
    
    # Только знаки препинания
    punctuation_text = "! ? . !!! ??? ..."
    chunks = splitter.split_text(punctuation_text)
    assert len(chunks) >= 1

if __name__ == "__main__":
    # Запуск тестов
    print("🧪 Запуск тестов TextSplitter...")
    
    try:
        test_text_splitter_basic()
        print("✅ Базовые тесты пройдены")
        
        test_text_splitter_long_text()
        print("✅ Тест длинного текста пройден")
        
        test_text_splitter_overlap()
        print("✅ Тест перекрытия пройден")
        
        test_text_splitter_sentence_boundaries()
        print("✅ Тест границ предложений пройден")
        
        test_text_splitter_clean_text()
        print("✅ Тест очистки текста пройден")
        
        test_text_splitter_unicode()
        print("✅ Тест Unicode пройден")
        
        test_text_splitter_edge_cases()
        print("✅ Тест граничных случаев пройден")
        
        print("\n🎉 Все тесты TextSplitter успешно пройдены!")
        
    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()