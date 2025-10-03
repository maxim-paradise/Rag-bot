"""
LLM Service - сервис для генерации ответов с помощью языковых моделей
"""
from typing import List, Dict, Any, Optional
import os
from dataclasses import dataclass

@dataclass
class ChatMessage:
    role: str  # 'system', 'user', 'assistant'
    content: str

class LLMService:
    def __init__(self, provider: str = "local", model: str = "microsoft/DialoGPT-medium"):
        """
        Инициализация LLM сервиса
        
        Args:
            provider: Провайдер LLM ('openai', 'anthropic', 'local')
            model: Название модели
        """
        self.provider = provider
        self.model = model
        self.client = None
        
        print(f"Инициализируем LLM сервис: {provider} - {model}")
        
        if provider == "openai":
            self._init_openai()
        elif provider == "anthropic":
            self._init_anthropic()
        elif provider == "local":
            self._init_local()
        else:
            print(f"⚠️ Неизвестный провайдер: {provider}. Используем заглушку.")
    
    def _init_openai(self):
        """Инициализация OpenAI"""
        try:
            import openai
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("⚠️ OPENAI_API_KEY не найден. Используем заглушку.")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI клиент инициализирован")
            
        except ImportError:
            print("⚠️ Библиотека openai не установлена. Установите: pip install openai")
        except Exception as e:
            print(f"⚠️ Ошибка инициализации OpenAI: {e}")
    
    def _init_anthropic(self):
        """Инициализация Anthropic Claude"""
        try:
            import anthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                print("⚠️ ANTHROPIC_API_KEY не найден. Используем заглушку.")
                return
            
            self.client = anthropic.Anthropic(api_key=api_key)
            print("✅ Anthropic клиент инициализирован")
            
        except ImportError:
            print("⚠️ Библиотека anthropic не установлена. Установите: pip install anthropic")
        except Exception as e:
            print(f"⚠️ Ошибка инициализации Anthropic: {e}")
    
    def _init_local(self):
        """Инициализация локальной модели"""
        try:
            from transformers import pipeline, AutoTokenizer
            
            print("🔄 Загружаем локальную модель...")
            
            # Загружаем модель и токенайзер отдельно для лучшего контроля
            model_name = "microsoft/DialoGPT-medium"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Устанавливаем pad_token если его нет
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            self.client = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=tokenizer,
                return_full_text=False  # Возвращаем только сгенерированный текст
            )
            print("✅ Локальная модель загружена")
            
        except ImportError:
            print("⚠️ Библиотека transformers не установлена.")
        except Exception as e:
            print(f"⚠️ Ошибка загрузки локальной модели: {e}")
    
    def generate_rag_response(self, question: str, context: str, sources: List[Dict]) -> str:
        """
        Генерация ответа на основе контекста (RAG)
        
        Args:
            question: Вопрос пользователя
            context: Контекст из найденных документов
            sources: Источники информации
            
        Returns:
            Сгенерированный ответ
        """
        if not self.client:
            return self._fallback_rag_response(question, context, sources)
        
        try:
            if self.provider == "openai":
                return self._openai_rag_response(question, context, sources)
            elif self.provider == "anthropic":
                return self._anthropic_rag_response(question, context, sources)
            elif self.provider == "local":
                return self._local_rag_response(question, context, sources)
            else:
                return self._fallback_rag_response(question, context, sources)
                
        except Exception as e:
            print(f"❌ Ошибка генерации ответа: {e}")
            return self._fallback_rag_response(question, context, sources)
    
    def generate_chat_response(self, messages: List[ChatMessage]) -> str:
        """
        Генерация ответа в обычном чате (без RAG)
        
        Args:
            messages: История сообщений
            
        Returns:
            Сгенерированный ответ
        """
        if not self.client:
            return self._fallback_chat_response(messages)
        
        try:
            if self.provider == "openai":
                return self._openai_chat_response(messages)
            elif self.provider == "anthropic":
                return self._anthropic_chat_response(messages)
            elif self.provider == "local":
                return self._local_chat_response(messages)
            else:
                return self._fallback_chat_response(messages)
                
        except Exception as e:
            print(f"❌ Ошибка генерации ответа: {e}")
            return self._fallback_chat_response(messages)
    
    def _openai_rag_response(self, question: str, context: str, sources: List[Dict]) -> str:
        """Генерация RAG ответа через OpenAI"""
        system_prompt = """Ты - умный помощник, который отвечает на вопросы на основе предоставленных документов.

Правила:
1. Отвечай только на основе предоставленного контекста
2. Если информации недостаточно, так и скажи
3. Отвечай на русском языке
4. Будь точным и информативным
5. Указывай, если что-то неясно из контекста"""

        user_prompt = f"""Вопрос: {question}

Контекст из документов:
{context}

Ответь на вопрос на основе этого контекста."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _openai_chat_response(self, messages: List[ChatMessage]) -> str:
        """Генерация обычного чата через OpenAI"""
        openai_messages = [
            {"role": msg.role, "content": msg.content} 
            for msg in messages
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            max_tokens=1000,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    def _anthropic_rag_response(self, question: str, context: str, sources: List[Dict]) -> str:
        """Генерация RAG ответа через Anthropic"""
        prompt = f"""Ты - умный помощник, который отвечает на вопросы на основе документов.

Вопрос: {question}

Контекст из документов:
{context}

Ответь на вопрос на основе этого контекста на русском языке."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def _anthropic_chat_response(self, messages: List[ChatMessage]) -> str:
        """Генерация обычного чата через Anthropic"""
        anthropic_messages = [
            {"role": msg.role, "content": msg.content} 
            for msg in messages if msg.role != "system"
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=anthropic_messages
        )
        
        return response.content[0].text
    
    def _local_rag_response(self, question: str, context: str, sources: List[Dict]) -> str:
        """Генерация RAG ответа через локальную модель"""
        # Сокращаем контекст чтобы избежать превышения лимитов
        max_context_length = 300
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        prompt = f"Вопрос: {question}\nКонтекст: {context}\nОтвет:"
        
        try:
            response = self.client(
                prompt, 
                max_new_tokens=100,  # Генерируем до 100 новых токенов
                num_return_sequences=1,
                truncation=True,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            generated_text = response[0]['generated_text']
            # Извлекаем только ответ после "Ответ:"
            if "Ответ:" in generated_text:
                answer = generated_text.split("Ответ:")[-1].strip()
            else:
                answer = generated_text.strip()
            
            # Если ответ пустой или слишком короткий, используем fallback
            if len(answer) < 10:
                return self._fallback_rag_response(question, context, sources)
            
            return answer
            
        except Exception as e:
            print(f"⚠️ Ошибка генерации RAG ответа: {e}")
            return self._fallback_rag_response(question, context, sources)
    
    def _local_chat_response(self, messages: List[ChatMessage]) -> str:
        """Генерация обычного чата через локальную модель"""
        last_message = messages[-1].content if messages else "Привет"
        
        try:
            response = self.client(
                last_message, 
                max_new_tokens=80,  # Генерируем до 80 новых токенов
                num_return_sequences=1,
                truncation=True,
                do_sample=True,
                temperature=0.8,
                top_p=0.9
            )
            
            generated_text = response[0]['generated_text']
            answer = generated_text.strip()
            
            # Если ответ пустой или слишком короткий, используем fallback
            if len(answer) < 5:
                return self._fallback_chat_response(messages)
            
            return answer
            
        except Exception as e:
            print(f"⚠️ Ошибка генерации чат ответа: {e}")
            return self._fallback_chat_response(messages)
    
    def _fallback_rag_response(self, question: str, context: str, sources: List[Dict]) -> str:
        """Заглушка для RAG ответов"""
        return f"На основе найденных документов: {context[:300]}{'...' if len(context) > 300 else ''}"
    
    def _fallback_chat_response(self, messages: List[ChatMessage]) -> str:
        """Заглушка для обычного чата"""
        return "Извините, LLM сервис не настроен. Обратитесь к администратору."
    
    def get_status(self) -> Dict[str, Any]:
        """Получить статус LLM сервиса"""
        return {
            "provider": self.provider,
            "model": self.model,
            "client_available": self.client is not None,
            "status": "ready" if self.client else "fallback"
        }