import re
from typing import List

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_text(self, text: str) -> List[str]:
        """
        Умное разбиение текста на чанки с перекрытием
        
        Args:
            text: Исходный текст для разбиения
            
        Returns:
            Список текстовых чанков
        """
        if not text:
            return []
            
        # Всегда очищаем текст, даже если он короткий
        text = self._clean_text(text)
        
        if len(text) <= self.chunk_size:
            return [text]

        sentences = self._split_into_sentences(text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Если добавление предложения не превышает лимит
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                # Сохраняем текущий чанк, если он не пустой
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                # Начинаем новый чанк с текущего предложения
                current_chunk = sentence + " "
                
                # Если предложение само по себе больше chunk_size, 
                # разбиваем его принудительно
                if len(current_chunk) > self.chunk_size:
                    # Принудительное разбиение длинного предложения
                    forced_chunks = self._force_split_long_text(current_chunk.strip())
                    chunks.extend(forced_chunks[:-1])  # Добавляем все кроме последнего
                    current_chunk = forced_chunks[-1] if forced_chunks else ""
        
        # Добавляем последний чанк
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        if self.overlap > 0 and len(chunks) > 1:
            chunks = self._add_overlap(chunks)

        return chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Очистка текста от лишних символов и форматирования
        """
        # Удаляем множественные пробелы, переносы строк и табуляции
        text = re.sub(r'\s+', ' ', text)
        # Удаляем лишние пробелы в начале и конце
        text = text.strip()
        return text

    def _split_into_sentences(self, text: str) -> List[str]:
        """Разбиение текста на предложения"""
        # Простое разбиение по знакам препинания
        # Можно улучшить с помощью библиотеки nltk или spacy
        sentences = re.split(r'[.!?]+', text)

        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Добавляем знак препинания обратно
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                clean_sentences.append(sentence)
        
        return clean_sentences
    
    def _add_overlap(self, chunks: List[str]) -> List[str]:
        """Добавление перекрытия между чанками"""
        if len(chunks) <= 1:
            return chunks
        
        overlapped_chunks = []
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                # Первый чанк без перекрытия
                overlapped_chunks.append(chunk.strip())
            else:
                # Добавляем перекрытие с предыдущим чанком
                prev_chunk = chunks[i-1]
                overlap_text = self._get_overlap_text(prev_chunk, self.overlap)
                
                if overlap_text:
                    overlapped_chunk = (overlap_text + " " + chunk).strip()
                    overlapped_chunks.append(overlapped_chunk)
                else:
                    overlapped_chunks.append(chunk.strip())
        
        return overlapped_chunks

    def _get_overlap_text(self, text: str, overlap_size: int) -> str:
        """Извлечение текста для перекрытия из конца строки"""
        words = text.split()
        if len(words) <= 2:  # Слишком короткий текст для перекрытия
            return ""
        
        overlap_words = []
        current_length = 0
        
        # Берем слова с конца текста
        for word in reversed(words):
            if current_length + len(word) + 1 > overlap_size:  # +1 для пробела
                break
            overlap_words.insert(0, word)
            current_length += len(word) + 1
        
        return " ".join(overlap_words)

    def _force_split_long_text(self, text: str) -> List[str]:
        """Принудительное разбиение длинного текста"""
        if len(text) <= self.chunk_size:
            return [text]
        
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 для пробела
            
            if current_length + word_length > self.chunk_size and current_chunk:
                # Сохраняем текущий чанк
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        # Добавляем последний чанк
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

        