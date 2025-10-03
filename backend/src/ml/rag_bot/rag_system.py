"""
RAG System
"""

from typing import List, Dict, Any, Optional

# Импорты с проверкой на относительные/абсолютные
try:
    from .embeddings_service import EmbeddingsService
    from .vector_store import VectorStore
    from .document_loader import DocumentLoader, Document
    from .text_splitter import TextSplitter
    from .llm_service import LLMService, ChatMessage
except ImportError:
    # Если относительные импорты не работают, используем абсолютные
    from ml.rag_bot.embeddings_service import EmbeddingsService
    from ml.rag_bot.vector_store import VectorStore
    from ml.rag_bot.document_loader import DocumentLoader, Document
    from ml.rag_bot.text_splitter import TextSplitter
    from ml.rag_bot.llm_service import LLMService, ChatMessage

class RAGSystem:
    def __init__(self, 
                embeddings_model: str = "cointegrated/rubert-tiny2",
                llm_provider: str = "local",
                llm_model: str = "microsoft/DialoGPT-medium",
                chunk_size: int = 1000,
                 overlap: int = 200):
        """
        Инициализация RAG системы
        
        Args:
            embeddings_model: Модель для создания эмбеддингов
            llm_provider: Провайдер LLM ('openai', 'anthropic', 'local')
            llm_model: Модель LLM
            chunk_size: Размер чанка для разбиения текста
            overlap: Перекрытие между чанками
        """
        print("🚀 Инициализация RAG системы...")

                # Инициализируем все компоненты
        self.embeddings_service = EmbeddingsService(embeddings_model)
        self.vector_store = VectorStore()
        self.document_loader = DocumentLoader()
        self.text_splitter = TextSplitter(chunk_size=chunk_size, overlap=overlap)
        self.llm_service = LLMService(provider=llm_provider, model=llm_model)
        
        print("✅ RAG система готова к работе")

    def load_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Загрузка и индексация документов
        
        Args:
            file_paths: Список путей к файлам
            
        Returns:
            Результат загрузки с метриками
        """
        print(f"📚 Загружаем {len(file_paths)} документов...")


        total_documents = 0
        total_chunks = 0 
        errors = []

        for file_path in file_paths:
            try:
                # Load Document
                document = self.document_loader.load_file(file_path)
                total_documents += 1

                # Split into chunks
                chunks = self.text_splitter.split_text(document.content)
                total_chunks += len(chunks)

                # Create embeddings
                embeddings = self.embeddings_service.encode_batch(chunks)

                # Add to vector store
                metadata_list = []

                for i, chunk in enumerate(chunks):
                    metadata = {
                        **document.metadata,
                        "chunk_index": i,
                        "chunk_size": len(chunk),
                        "total_chunks": len(chunks),
                    }
                    metadata_list.append(metadata)

                # add vector db
                self.vector_store.add_documents(chunks, embeddings, metadata_list)

                print(f"✅ {document.metadata['filename']}: {len(chunks)} чанков")
            
            except Exception as e:
                error_msg = f"Ошибка загрузки {file_path}: {e}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        result = {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "errors": errors,
            "success": len(errors) == 0
        }
        
        print(f"📊 Загрузка завершена: {total_documents} документов, {total_chunks} чанков")
        return result
                
    def ask(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Задать вопрос RAG системе
        
        Args:
            question: Вопрос пользователя
            top_k: Количество релевантных документов для поиска
            
        Returns:
            Ответ с источниками и метаданными
        """
        print(f"💬 Задаем вопрос: {question}")

        try:
            # Search for vector db
            question_embedding = self.embeddings_service.encode(question)

            # Search for relevant documents
            search_results = self.vector_store.search(question_embedding, top_k=top_k)

            
            if not search_results:
                return {
                    "answer": "К сожалению, не удалось найти релевантную информацию в базе знаний.",
                    "sources": [],
                    "question": question,
                    "status": "no_results"
                }
            
            # 3. Подготовка контекста
            context_parts = []
            sources = []

            for result in search_results:
                context_parts.append(result['document'])
                sources.append({
                    "id": result['id'],
                    "similarity": result['similarity'],
                    "metadata": result['metadata']
                })
            
            context = "\n\n".join(context_parts)

            # generate answer
            answer = self.llm_service.generate_rag_response(question, context, sources)

            result = {
                "answer": answer,
                "sources": sources,
                "question": question,
                "context_length": len(context),
                "sources_count": len(sources),
                "status": "success"
            }

            print(f"✅ Ответ сгенерирован на основе {len(sources)} источников")
            return result
            
        except Exception as e:
            error_msg = f"Ошибка обработки вопроса: {e}"
            print(f"❌ {error_msg}")
            
            return {
                "answer": "Произошла ошибка при обработке вопроса. Попробуйте переформулировать.",
                "sources": [],
                "question": question,
                "error": error_msg,
                "status": "error"
            }

    
    def chat(self, message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Чат с системой (с контекстом из истории)
        
        Args:
            message: Новое сообщение
            history: История сообщений [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            Ответ с источниками и метаданными
        """

        if history is None:
            history = []
        
        # Сначала пытаемся ответить через RAG
        rag_response = self.ask(message)


        # Если RAG дал хороший ответ, используем его
        if rag_response["status"] == "success" and rag_response["sources_count"] > 0:
            return {
                "answer": rag_response["answer"],
                "sources": rag_response["sources"],
                "type": "rag",
                "status": "success"
            }

        #else using just chat
        messages = []

        # Add history
        for msg in history[-5:]: #limit to last 5 messages
            messages.append(ChatMessage(role=msg["role"], content=msg["content"]))

        # Добавляем текущее сообщение
        messages.append(ChatMessage(role="user", content=message))
        
        # Генерируем ответ
        answer = self.llm_service.generate_chat_response(messages)
        
        return {
            "answer": answer,
            "sources": [],
            "type": "chat",
            "status": "success"
        }
        
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Поиск в векторной базе без генерации ответа
        
        Args:
            query: Поисковый запрос
            top_k: Количество результатов
            
        Returns:
            Список найденных документов
        """
        try:
            query_embedding = self.embeddings_service.encode(query)
            results = self.vector_store.search(query_embedding, top_k=top_k)
            
            return results
            
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
            return []
    def get_status(self) -> Dict[str, Any]:
        """
        Получение статуса системы
        
        Returns:
            Статус системы
        """
        return {
            "embeddings_service": {
                "model": self.embeddings_service.model_name,
                "status": "ready"
            },
            "vector_store": self.vector_store.get_collection_info(),
            "llm_service": self.llm_service.get_status(),
            "text_splitter": {
                "chunk_size": self.text_splitter.chunk_size,
                "overlap": self.text_splitter.overlap
            },
            "system_status": "ready"
        }
    def clear_database(self) -> bool:
        """Очистить векторную базу данных"""
        return self.vector_store.clear_collection()
