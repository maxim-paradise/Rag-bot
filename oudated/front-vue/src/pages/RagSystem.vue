<template>
  <div class="h-screen bg-background flex">
    <!-- Левая панель - Управление документами -->
    <div class="w-80 border-r border-border bg-card flex flex-col">
      <!-- Заголовок -->
      <div class="p-4 border-b border-border">
        <h1 class="text-xl font-semibold text-foreground flex items-center gap-2">
          <FileText class="w-5 h-5" />
          RAG Система
        </h1>
        <p class="text-sm text-muted-foreground mt-1">
          Загружайте документы и задавайте вопросы
        </p>
      </div>

      <!-- Статус системы -->
      <div class="p-4 border-b border-border">
        <div class="flex items-center gap-2 mb-2">
          <div :class="[
            'w-2 h-2 rounded-full',
            systemStatus === 'healthy' ? 'bg-green-500' : 'bg-red-500'
          ]" />
          <span class="text-sm font-medium">
            {{ systemStatus === 'healthy' ? 'Система работает' : 'Ошибка системы' }}
          </span>
        </div>
        <div class="text-xs text-muted-foreground space-y-1">
          <div>Документов: {{ documentsCount }}</div>
          <div>Модель: {{ embeddingsModel }}</div>
        </div>
      </div>

      <!-- Загрузка документов -->
      <div class="p-4 border-b border-border">
        <h3 class="font-medium mb-3 flex items-center gap-2">
          <Upload class="w-4 h-4" />
          Загрузить документы
        </h3>
        
        <div
          @drop="handleDrop"
          @dragover.prevent
          @dragenter.prevent
          :class="[
            'border-2 border-dashed rounded-lg p-4 text-center transition-colors cursor-pointer',
            isDragOver ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
          ]"
          @click="triggerFileInput"
          @dragenter="isDragOver = true"
          @dragleave="isDragOver = false"
        >
          <input
            ref="fileInput"
            type="file"
            multiple
            accept=".txt,.md,.pdf,.docx,.doc,.py,.js,.html,.css"
            @change="handleFileSelect"
            class="hidden"
          />
          
          <Upload class="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
          <p class="text-sm text-muted-foreground">
            Перетащите файлы или нажмите для выбора
          </p>
          <p class="text-xs text-muted-foreground mt-1">
            TXT, MD, PDF, DOCX, PY, JS, HTML, CSS
          </p>
        </div>

        <!-- Прогресс загрузки -->
        <div v-if="uploadProgress.length > 0" class="mt-3 space-y-2">
          <div v-for="progress in uploadProgress" :key="progress.filename" 
               class="text-xs bg-muted rounded p-2">
            <div class="flex justify-between items-center">
              <span class="truncate">{{ progress.filename }}</span>
              <span :class="[
                progress.status === 'success' ? 'text-green-600' : 
                progress.status === 'error' ? 'text-red-600' : 'text-blue-600'
              ]">
                {{ progress.status === 'uploading' ? 'Загрузка...' : 
                   progress.status === 'success' ? 'Готово' : 'Ошибка' }}
              </span>
            </div>
            <div v-if="progress.error" class="text-red-600 mt-1">
              {{ progress.error }}
            </div>
          </div>
        </div>
      </div>

      <!-- Список документов -->
      <div class="flex-1 overflow-hidden flex flex-col">
        <div class="p-4 border-b border-border">
          <h3 class="font-medium flex items-center gap-2">
            <FileText class="w-4 h-4" />
            Документы ({{ documents.length }})
          </h3>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 space-y-2">
          <div v-if="documentsLoading" class="text-center py-8">
            <Loader2 class="w-6 h-6 animate-spin mx-auto mb-2" />
            <p class="text-sm text-muted-foreground">Загрузка документов...</p>
          </div>
          
          <div v-else-if="documents.length === 0" class="text-center py-8">
            <FileText class="w-12 h-12 mx-auto mb-3 text-muted-foreground" />
            <p class="text-sm text-muted-foreground">Нет загруженных документов</p>
          </div>
          
          <div v-else>
            <div v-for="doc in documents" :key="doc.id" 
                 class="bg-muted rounded-lg p-3 hover:bg-muted/80 transition-colors group">
              <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                  <h4 class="font-medium text-sm truncate">{{ doc.filename }}</h4>
                  <p class="text-xs text-muted-foreground mt-1">
                    {{ formatFileSize(doc.content_length) }} • {{ doc.file_extension }}
                  </p>
                  <p v-if="doc.content_preview" class="text-xs text-muted-foreground mt-1 line-clamp-2">
                    {{ doc.content_preview }}
                  </p>
                </div>
                <button
                  @click="deleteDocument(doc.id)"
                  class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-destructive/10 rounded"
                  :disabled="deletingDocuments.has(doc.id)"
                >
                  <Trash2 class="w-4 h-4 text-destructive" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Правая панель - Чат -->
    <div class="flex-1 flex flex-col">
      <!-- Заголовок чата -->
      <div class="p-4 border-b border-border bg-card">
        <h2 class="font-semibold flex items-center gap-2">
          <MessageSquare class="w-5 h-5" />
          Чат с документами
        </h2>
        <p class="text-sm text-muted-foreground">
          Задавайте вопросы по загруженным документам
        </p>
      </div>

      <!-- Сообщения чата -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
        <div v-if="messages.length === 0" class="text-center py-12">
          <MessageSquare class="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
          <h3 class="text-lg font-medium mb-2">Начните разговор</h3>
          <p class="text-muted-foreground mb-4">
            Загрузите документы и задайте вопрос для получения ответов на основе их содержания
          </p>
          <div class="flex flex-wrap gap-2 justify-center">
            <button
              v-for="example in exampleQuestions"
              :key="example"
              @click="sendMessage(example)"
              class="px-3 py-1 text-sm bg-muted hover:bg-muted/80 rounded-full transition-colors"
            >
              {{ example }}
            </button>
          </div>
        </div>

        <div v-for="message in messages" :key="message.id" 
             :class="[
               'flex gap-3',
               message.type === 'user' ? 'justify-end' : 'justify-start'
             ]">
          <div :class="[
            'max-w-[80%] rounded-lg p-4',
            message.type === 'user' 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-muted'
          ]">
            <div class="flex items-start gap-2 mb-2">
              <div :class="[
                'w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium',
                message.type === 'user' 
                  ? 'bg-primary-foreground/20 text-primary-foreground' 
                  : 'bg-primary text-primary-foreground'
              ]">
                {{ message.type === 'user' ? 'Вы' : 'AI' }}
              </div>
              <div class="text-xs text-muted-foreground">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
            
            <div class="prose prose-sm max-w-none">
              <p class="whitespace-pre-wrap">{{ message.content }}</p>
            </div>

            <!-- Источники для ответов ассистента -->
            <div v-if="message.sources && message.sources.length > 0" class="mt-3 pt-3 border-t border-border/20">
              <p class="text-xs font-medium mb-2">Источники:</p>
              <div class="space-y-2">
                <div v-for="source in message.sources" :key="source.id" 
                     class="text-xs bg-background/50 rounded p-2">
                  <div class="flex justify-between items-center mb-1">
                    <span class="font-medium">{{ source.metadata.filename || 'Документ' }}</span>
                    <span class="text-muted-foreground">{{ (source.similarity * 100).toFixed(1) }}%</span>
                  </div>
                  <p class="text-muted-foreground line-clamp-2">{{ source.document }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Индикатор печатания -->
        <div v-if="isTyping" class="flex gap-3">
          <div class="bg-muted rounded-lg p-4 max-w-[80%]">
            <div class="flex items-center gap-2">
              <Loader2 class="w-4 h-4 animate-spin" />
              <span class="text-sm text-muted-foreground">AI печатает...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Поле ввода -->
      <div class="p-4 border-t border-border bg-card">
        <div class="flex gap-2">
          <div class="flex-1 relative">
            <textarea
              v-model="currentMessage"
              @keydown.enter.prevent="handleEnterKey"
              :disabled="isTyping || documents.length === 0"
              placeholder="Задайте вопрос по документам..."
              class="w-full resize-none rounded-lg border border-border bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent disabled:opacity-50"
              rows="1"
              ref="messageInput"
            />
            <div class="absolute right-2 top-2 text-xs text-muted-foreground">
              Enter для отправки
            </div>
          </div>
          <button
            @click="sendMessage()"
            :disabled="!currentMessage.trim() || isTyping || documents.length === 0"
            class="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send class="w-4 h-4" />
          </button>
        </div>
        
        <div v-if="documents.length === 0" class="text-xs text-muted-foreground mt-2">
          Загрузите документы, чтобы начать чат
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { 
  FileText, Upload, MessageSquare, Send, Loader2, Trash2 
} from 'lucide-vue-next'
import { ragApi, type Document, type ChatMessage, type SearchResult } from '@/api/ragApi'

// Реактивные данные
const systemStatus = ref<'healthy' | 'error'>('error')
const documentsCount = ref(0)
const embeddingsModel = ref('')
const documents = ref<Document[]>([])
const documentsLoading = ref(false)
const deletingDocuments = ref(new Set<string>())

const messages = ref<ChatMessage[]>([])
const currentMessage = ref('')
const isTyping = ref(false)
const isDragOver = ref(false)

const uploadProgress = ref<Array<{
  filename: string
  status: 'uploading' | 'success' | 'error'
  error?: string
}>>([])

// Refs
const fileInput = ref<HTMLInputElement>()
const messageInput = ref<HTMLTextAreaElement>()
const chatContainer = ref<HTMLElement>()

// Примеры вопросов
const exampleQuestions = [
  'О чем этот документ?',
  'Какие основные темы рассматриваются?',
  'Есть ли примеры кода?',
  'Какие выводы можно сделать?'
]

// Методы
const checkSystemHealth = async () => {
  try {
    const health = await ragApi.healthCheck()
    systemStatus.value = health.status === 'healthy' ? 'healthy' : 'error'
    documentsCount.value = health.documents_count || 0
    embeddingsModel.value = health.embeddings_model || ''
  } catch (error) {
    console.error('Health check failed:', error)
    systemStatus.value = 'error'
  }
}

const loadDocuments = async () => {
  documentsLoading.value = true
  try {
    const response = await ragApi.getDocuments()
    documents.value = response.documents
    documentsCount.value = response.total_documents
  } catch (error) {
    console.error('Failed to load documents:', error)
  } finally {
    documentsLoading.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    uploadFiles(Array.from(target.files))
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  
  if (event.dataTransfer?.files) {
    uploadFiles(Array.from(event.dataTransfer.files))
  }
}

const uploadFiles = async (files: File[]) => {
  // Инициализируем прогресс
  uploadProgress.value = files.map(file => ({
    filename: file.name,
    status: 'uploading' as const
  }))

  try {
    const result = await ragApi.uploadDocuments(files)
    
    // Обновляем прогресс на основе результатов
    uploadProgress.value = result.results.map(r => ({
      filename: r.filename,
      status: r.status,
      error: r.error
    }))

    // Перезагружаем список документов
    await loadDocuments()
    await checkSystemHealth()

    // Очищаем прогресс через 3 секунды
    setTimeout(() => {
      uploadProgress.value = []
    }, 3000)

  } catch (error) {
    console.error('Upload failed:', error)
    uploadProgress.value = uploadProgress.value.map(p => ({
      ...p,
      status: 'error' as const,
      error: 'Ошибка загрузки'
    }))
  }
}

const deleteDocument = async (docId: string) => {
  deletingDocuments.value.add(docId)
  try {
    await ragApi.deleteDocument(docId)
    await loadDocuments()
    await checkSystemHealth()
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    deletingDocuments.value.delete(docId)
  }
}

const sendMessage = async (messageText?: string) => {
  const text = messageText || currentMessage.value.trim()
  if (!text || isTyping.value) return

  // Добавляем сообщение пользователя
  const userMessage: ChatMessage = {
    id: Date.now().toString(),
    type: 'user',
    content: text,
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  currentMessage.value = ''

  // Скроллим к низу
  await nextTick()
  chatContainer.value?.scrollTo({ top: chatContainer.value.scrollHeight, behavior: 'smooth' })

  isTyping.value = true

  try {
    const response = await ragApi.chatWithDocuments(text)
    
    // Добавляем ответ ассистента
    const assistantMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: response.answer,
      timestamp: new Date(),
      sources: response.sources
    }
    messages.value.push(assistantMessage)

  } catch (error) {
    console.error('Chat failed:', error)
    
    const errorMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: 'Извините, произошла ошибка при обработке вашего запроса. Попробуйте еще раз.',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    await nextTick()
    chatContainer.value?.scrollTo({ top: chatContainer.value.scrollHeight, behavior: 'smooth' })
  }
}

const handleEnterKey = (event: KeyboardEvent) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString('ru-RU', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Инициализация
onMounted(async () => {
  await checkSystemHealth()
  await loadDocuments()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prose p {
  margin: 0;
}
</style>