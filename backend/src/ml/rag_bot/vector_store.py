"""
Vector Store - работа с векторной базой данных
"""
from typing import List, Dict, Any
import chromadb
from pathlib import Path
import uuid

class VectorStore:
    def __init__(self, db_path: str = "./data/vector_db", collection_name: str = "documents"):
        self.db_path = db_path
        self.collection_name = collection_name

        Path(db_path).mkdir(parents=True, exist_ok=True)

        print(f"Инициализируем ChromaDB в {db_path}")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)
        print(f"Коллекция '{collection_name}' готова")
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadata: List[Dict]) -> List[str]:
        """
        Добавить документы в векторную БД
        
        Args:
            documents: Список текстов документов
            embeddings: Список векторов для каждого документа
            metadata: Метаданные для каждого документа
            
        Returns:
            Список ID добавленных документов
        """

        if len(documents) != len(embeddings) or len(documents) != len(metadata):
            raise ValueError("Lengths of documents, embeddings, and metadata must match")

        doc_ids = [str(uuid.uuid4()) for _ in documents]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
            ids=doc_ids
        )
        print(f"Добавлено {len(documents)} документов в векторную БД")
        return doc_ids

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Поиск похожих документов
        
        Args:
            query_embedding: Вектор запроса
            top_k: Количество результатов
            
        Returns:
            Список найденных документов с метаданными и скорами
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        formatted_results = []

        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'][0] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'similarity': 1 - results['distances'][0][i] if results['distances'] else None
                })

        return formatted_results
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Удалить документ по ID
        
        Args:
            doc_id: ID документа для удаления
            
        Returns:
            True если удален успешно
        """
        try:
            self.collection.delete(ids=[doc_id])
            print(f"Документ {doc_id} удален")
            return True
        except Exception as e:
            print(f"Ошибка удаления документа {doc_id}: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Получить информацию о коллекции"""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "documents_count": count,
            "db_path": self.db_path
        }
    
    def clear_collection(self) -> bool:
        """Очистить всю коллекцию"""
        try:
            # Получаем все ID и удаляем
            all_data = self.collection.get()
            if all_data['ids']:
                self.collection.delete(ids=all_data['ids'])
            print(f"Коллекция '{self.collection_name}' очищена")
            return True
        except Exception as e:
            print(f"Ошибка очистки коллекции: {e}")
            return False