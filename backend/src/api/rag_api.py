"""
RAG API - эндпоинты для работы с RAG системой
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import tempfile
import os
from pathlib import Path

# Импортируем наши RAG компоненты
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ml.rag_bot.rag_system import RAGSystem

router = APIRouter(tags=["RAG System"])

# Глобальная RAG система (инициализируется при запуске)
rag_system = None

# Pydantic модели для API
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    document: str
    similarity: float
    metadata: dict
    id: str

class ChatRequest(BaseModel):
    question: str
    top_k: int = 3

class ChatResponse(BaseModel):
    answer: str
    sources: List[SearchResult]
    question: str

class SimpleChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class SimpleChatResponse(BaseModel):
    response: str
    message: str

class LLMConfigRequest(BaseModel):
    provider: str  # 'openai', 'anthropic', 'local'
    model: str
    api_key: Optional[str] = None

class DocumentInfo(BaseModel):
    filename: str
    content_length: int
    file_extension: str
    upload_time: str

def initialize_rag_system():
    """Инициализация RAG системы"""
    global rag_system
    
    if rag_system is None:
        print("🚀 Инициализируем RAG систему...")
        
        # Настройки из переменных окружения
        embeddings_model = os.getenv('EMBEDDINGS_MODEL', 'cointegrated/rubert-tiny2')
        llm_provider = os.getenv('LLM_PROVIDER', 'local')
        llm_model = os.getenv('LLM_MODEL', 'microsoft/DialoGPT-medium')
        chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
        overlap = int(os.getenv('CHUNK_OVERLAP', '200'))
        
        rag_system = RAGSystem(
            embeddings_model=embeddings_model,
            llm_provider=llm_provider,
            llm_model=llm_model,
            chunk_size=chunk_size,
            overlap=overlap
        )
        
        print("✅ RAG система готова!")

# Инициализация сервисов при импорте модуля
# initialize_rag_services()

@router.post("/documents/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Загрузка документов в RAG систему
    
    Args:
        files: Список файлов для загрузки
        
    Returns:
        Информация о загруженных документах
    """
    initialize_rag_system()
    
    # Сохраняем файлы во временную директорию
    temp_files = []
    uploaded_docs = []
    
    try:
        # Сохраняем все файлы
        for file in files:
            temp_file_path = tempfile.mktemp(suffix=Path(file.filename).suffix)
            content = await file.read()
            
            with open(temp_file_path, 'wb') as tmp_file:
                tmp_file.write(content)
            
            temp_files.append(temp_file_path)
        
        # Загружаем документы через RAG систему
        load_result = rag_system.load_documents(temp_files)
        
        # Формируем ответ
        for i, file in enumerate(files):
            if load_result["success"]:
                uploaded_docs.append({
                    "filename": file.filename,
                    "status": "success",
                    "content_length": len(open(temp_files[i], 'r', encoding='utf-8').read()) if i < len(temp_files) else 0
                })
            else:
                uploaded_docs.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": "Ошибка загрузки документа"
                })
        
        return {
            "message": f"Обработано {len(files)} файлов",
            "results": uploaded_docs,
            "total_documents": load_result["total_documents"],
            "total_chunks": load_result["total_chunks"]
        }
        
    except Exception as e:
        return {
            "message": f"Ошибка обработки файлов: {str(e)}",
            "results": uploaded_docs
        }
        
    finally:
        # Удаляем временные файлы
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

@router.post("/search", response_model=List[SearchResult])
async def search_documents(request: SearchRequest):
    """
    Поиск документов по запросу
    
    Args:
        request: Запрос с текстом для поиска
        
    Returns:
        Список найденных документов
    """
    initialize_rag_system()
    
    try:
        # Ищем документы через RAG систему
        results = rag_system.search(request.query, top_k=request.top_k)
        
        # Форматируем результаты
        search_results = []
        for result in results:
            search_results.append(SearchResult(
                document=result['document'],
                similarity=result['similarity'],
                metadata=result['metadata'],
                id=result['id']
            ))
        
        return search_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_documents(request: ChatRequest):
    """
    Чат с документами (RAG)
    
    Args:
        request: Вопрос пользователя
        
    Returns:
        Ответ на основе документов
    """
    initialize_rag_system()
    
    try:
        # Используем RAG систему для генерации ответа
        response = rag_system.ask(request.question, top_k=request.top_k)
        
        # Форматируем источники
        sources = []
        for source in response.get("sources", []):
            sources.append(SearchResult(
                document=source["metadata"].get("document", "")[:200] + "..." if len(source["metadata"].get("document", "")) > 200 else source["metadata"].get("document", ""),
                similarity=source["similarity"],
                metadata=source["metadata"],
                id=source["id"]
            ))
        
        return ChatResponse(
            answer=response["answer"],
            sources=sources,
            question=request.question
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чата: {str(e)}")

@router.get("/documents/list")
async def list_documents():
    """
    Получить список всех документов в системе
    
    Returns:
        Список документов с метаданными
    """
    initialize_rag_system()
    
    try:
        # Получаем статус системы
        status = rag_system.get_status()
        
        # Получаем документы из векторной БД
        all_data = rag_system.vector_store.collection.get()
        
        documents = []
        if all_data['ids']:
            for i, doc_id in enumerate(all_data['ids']):
                metadata = all_data['metadatas'][i] if all_data['metadatas'] else {}
                documents.append({
                    "id": doc_id,
                    "filename": metadata.get('filename', 'Unknown'),
                    "content_length": metadata.get('content_length', 0),
                    "file_extension": metadata.get('file_extension', ''),
                    "chunk_index": metadata.get('chunk_index', 0),
                    "total_chunks": metadata.get('total_chunks', 1),
                    "content_preview": all_data['documents'][i][:100] + "..." if len(all_data['documents'][i]) > 100 else all_data['documents'][i]
                })
        
        return {
            "total_documents": status["vector_store"]["documents_count"],
            "documents": documents,
            "system_status": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка: {str(e)}")

@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Удалить документ из системы
    
    Args:
        doc_id: ID документа для удаления
        
    Returns:
        Статус удаления
    """
    initialize_rag_system()
    
    try:
        success = rag_system.vector_store.delete_document(doc_id)
        
        if success:
            return {"message": f"Документ {doc_id} успешно удален"}
        else:
            raise HTTPException(status_code=404, detail="Документ не найден")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления: {str(e)}")

@router.get("/health")
async def health_check():
    """Проверка состояния RAG системы"""
    initialize_rag_system()
    
    try:
        status = rag_system.get_status()
        
        return {
            "status": "healthy",
            "system_status": status["system_status"],
            "documents_count": status["vector_store"]["documents_count"],
            "embeddings_model": status["embeddings_service"]["model"],
            "llm_status": status["llm_service"]["status"],
            "llm_provider": status["llm_service"]["provider"]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.post("/simple-chat", response_model=SimpleChatResponse)
async def simple_chat(request: SimpleChatRequest):
    """
    Простой чат с AI (без документов)
    
    Args:
        request: Сообщение и история чата
        
    Returns:
        Ответ от AI
    """
    initialize_rag_system()
    
    try:
        # Используем RAG систему для чата
        response = rag_system.chat(request.message, request.history)
        
        return SimpleChatResponse(
            response=response["answer"],
            message=request.message
        )
        
    except Exception as e:
        print(f"❌ Ошибка в чате: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка чата: {str(e)}")

@router.get("/llm-status")
async def get_llm_status():
    """Получить статус LLM сервиса"""
    initialize_rag_system()
    
    try:
        status = rag_system.get_status()
        return status["llm_service"]
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

@router.post("/configure-llm")
async def configure_llm(config: LLMConfigRequest):
    """Настроить LLM провайдер"""
    global rag_system
    
    try:
        # Устанавливаем API ключ если предоставлен
        if config.api_key:
            if config.provider == "openai":
                os.environ['OPENAI_API_KEY'] = config.api_key
            elif config.provider == "anthropic":
                os.environ['ANTHROPIC_API_KEY'] = config.api_key
        
        # Пересоздаем RAG систему с новыми настройками
        rag_system = None  # Сбрасываем текущую систему
        initialize_rag_system()
        
        return {
            "status": "success",
            "message": f"LLM настроен: {config.provider} - {config.model}",
            "provider": config.provider,
            "model": config.model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка настройки LLM: {str(e)}")

@router.get("/llm-providers")
async def get_llm_providers():
    """Получить список доступных LLM провайдеров"""
    return {
        "providers": {
            "local": {
                "name": "Локальная модель",
                "models": [
                    "microsoft/DialoGPT-medium",
                    "microsoft/DialoGPT-small",
                    "gpt2"
                ],
                "requires_api_key": False,
                "description": "Работает без интернета, но медленно"
            },
            "openai": {
                "name": "OpenAI",
                "models": [
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-4-turbo-preview"
                ],
                "requires_api_key": True,
                "description": "Быстро и качественно, нужен API ключ"
            },
            "anthropic": {
                "name": "Anthropic Claude",
                "models": [
                    "claude-3-haiku-20240307",
                    "claude-3-sonnet-20240229",
                    "claude-3-opus-20240229"
                ],
                "requires_api_key": True,
                "description": "Очень умный, нужен API ключ"
            }
        }
    }

@router.delete("/clear-database")
async def clear_database():
    """Очистить всю базу данных документов"""
    initialize_rag_system()
    
    try:
        success = rag_system.clear_database()
        
        if success:
            return {"message": "База данных успешно очищена"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка очистки базы данных")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка очистки: {str(e)}")