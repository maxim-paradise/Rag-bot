<template>
  <div class="h-screen bg-background flex">
    <!-- Сайдбар -->
    <div :class="[
      'transition-all duration-300 ease-in-out bg-card border-r border-border flex flex-col',
      sidebarOpen ? 'w-80' : 'w-16'
    ]">
      <!-- Заголовок сайдбара -->
      <div class="p-4 border-b border-border">
        <div class="flex items-center justify-between">
          <div v-if="sidebarOpen" class="flex items-center gap-2">
            <Bot class="w-6 h-6 text-primary" />
            <h1 class="text-lg font-semibold">AI Система</h1>
          </div>
          <button
            @click="toggleSidebar"
            class="p-2 hover:bg-muted rounded-lg transition-colors"
          >
            <Menu v-if="!sidebarOpen" class="w-5 h-5" />
            <X v-else class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Режимы работы -->
      <div class="p-4 border-b border-border">
        <div v-if="sidebarOpen" class="space-y-2">
          <h3 class="text-sm font-medium text-muted-foreground mb-3">Режим работы</h3>
          <div class="space-y-1">
            <button
              @click="currentMode = 'chat'"
              :class="[
                'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
                currentMode === 'chat' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'hover:bg-muted'
              ]"
            >
              <MessageSquare class="w-4 h-4" />
              Простой чат
            </button>
            <button
              @click="currentMode = 'rag'"
              :class="[
                'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
                currentMode === 'rag' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'hover:bg-muted'
              ]"
            >
              <FileText class="w-4 h-4" />
              RAG с документами
            </button>
          </div>
        </div>
        <div v-else class="space-y-2">
          <button
            @click="currentMode = 'chat'"
            :class="[
              'w-full p-2 rounded-lg transition-colors',
              currentMode === 'chat' ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'
            ]"
            title="Простой чат"
          >
            <MessageSquare class="w-4 h-4" />
          </button>
          <button
            @click="currentMode = 'rag'"
            :class="[
              'w-full p-2 rounded-lg transition-colors',
              currentMode === 'rag' ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'
            ]"
            title="RAG с документами"
          >
            <FileText class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Статус системы -->
      <div class="p-4 border-b border-border">
        <div v-if="sidebarOpen" class="space-y-3">
          <h3 class="text-sm font-medium text-muted-foreground">Статус системы</h3>
          
          <!-- LLM статус -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm">LLM</span>
              <div class="flex items-center gap-2">
                <div :class="[
                  'w-2 h-2 rounded-full',
                  llmStatus?.status === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
                ]" />
                <span class="text-xs text-muted-foreground">
                  {{ llmStatus?.status === 'ready' ? 'Готов' : 'Заглушка' }}
                </span>
              </div>
            </div>
            <div class="text-xs text-muted-foreground">
              {{ llmStatus?.provider || 'Не определен' }} - {{ llmStatus?.model || 'Не определена' }}
            </div>
          </div>

          <!-- RAG статус (только в RAG режиме) -->
          <div v-if="currentMode === 'rag'" class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-sm">Документы</span>
              <span class="text-xs text-muted-foreground">{{ documentsCount }}</span>
            </div>
            <div class="text-xs text-muted-foreground">
              Embeddings: {{ embeddingsModel }}
            </div>
          </div>
        </div>
        <div v-else class="space-y-2">
          <div :class="[
            'w-2 h-2 rounded-full mx-auto',
            llmStatus?.status === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
          ]" title="Статус LLM" />
          <div v-if="currentMode === 'rag'" class="text-xs text-center text-muted-foreground">
            {{ documentsCount }}
          </div>
        </div>
      </div>

      <!-- Настройки -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-4">
          <div v-if="sidebarOpen">
            <h3 class="text-sm font-medium text-muted-foreground mb-3">Настройки</h3>
            
            <!-- Вкладки настроек -->
            <div class="space-y-1 mb-4">
              <button
                @click="activeSettingsTab = 'llm'"
                :class="[
                  'w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors',
                  activeSettingsTab === 'llm' 
                    ? 'bg-muted text-foreground' 
                    : 'hover:bg-muted/50 text-muted-foreground'
                ]"
              >
                <Bot class="w-4 h-4" />
                LLM Настройки
              </button>
              <button
                v-if="currentMode === 'rag'"
                @click="activeSettingsTab = 'documents'"
                :class="[
                  'w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors',
                  activeSettingsTab === 'documents' 
                    ? 'bg-muted text-foreground' 
                    : 'hover:bg-muted/50 text-muted-foreground'
                ]"
              >
                <Upload class="w-4 h-4" />
                Документы
              </button>
            </div>

            <!-- Содержимое настроек -->
            <div class="space-y-4">
              <!-- LLM Настройки -->
              <div v-if="activeSettingsTab === 'llm'">
                <LLMSettings @settings-applied="onLLMSettingsApplied" />
              </div>

              <!-- Управление документами -->
              <div v-if="activeSettingsTab === 'documents' && currentMode === 'rag'">
                <DocumentManager 
                  @documents-updated="onDocumentsUpdated"
                  @document-uploaded="onDocumentUploaded"
                />
              </div>
            </div>
          </div>
          <div v-else class="space-y-2">
            <button
              @click="activeSettingsTab = 'llm'; sidebarOpen = true"
              class="w-full p-2 hover:bg-muted rounded-lg transition-colors"
              title="LLM Настройки"
            >
              <Bot class="w-4 h-4" />
            </button>
            <button
              v-if="currentMode === 'rag'"
              @click="activeSettingsTab = 'documents'; sidebarOpen = true"
              class="w-full p-2 hover:bg-muted rounded-lg transition-colors"
              title="Документы"
            >
              <Upload class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Основная область чата -->
    <div class="flex-1 flex flex-col">
      <!-- Заголовок чата -->
      <div class="p-4 border-b border-border bg-card">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold flex items-center gap-2">
              <MessageSquare v-if="currentMode === 'chat'" class="w-5 h-5" />
              <FileText v-else class="w-5 h-5" />
              {{ currentMode === 'chat' ? 'AI Чат' : 'RAG Система' }}
            </h2>
            <p class="text-sm text-muted-foreground">
              {{ currentMode === 'chat' 
                ? 'Общайтесь с искусственным интеллектом' 
                : 'Задавайте вопросы по загруженным документам' 
              }}
            </p>
          </div>
          
          <button
            @click="clearChat"
            class="px-3 py-1 text-sm bg-muted hover:bg-muted/80 rounded-lg transition-colors"
          >
            Очистить чат
          </button>
        </div>
      </div>

      <!-- Сообщения чата -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
        <div v-if="messages.length === 0" class="text-center py-12">
          <div class="w-16 h-16 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
            <MessageSquare v-if="currentMode === 'chat'" class="w-8 h-8 text-muted-foreground" />
            <FileText v-else class="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 class="text-lg font-medium mb-2">Начните разговор</h3>
          <p class="text-muted-foreground mb-4">
            {{ currentMode === 'chat' 
              ? 'Задайте любой вопрос или просто поздоровайтесь' 
              : 'Загрузите документы в настройках и задайте вопрос' 
            }}
          </p>
          <div class="flex flex-wrap gap-2 justify-center">
            <button
              v-for="example in currentExamples"
              :key="example"
              @click="sendMessage(example)"
              :disabled="currentMode === 'rag' && documentsCount === 0"
              class="px-3 py-1 text-sm bg-muted hover:bg-muted/80 rounded-full transition-colors disabled:opacity-50"
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
                {{ message.type === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="text-xs text-muted-foreground">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
            
            <div class="prose prose-sm max-w-none">
              <p class="whitespace-pre-wrap">{{ message.content }}</p>
            </div>

            <!-- Источники для RAG ответов -->
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
              :disabled="isTyping || (currentMode === 'rag' && documentsCount === 0)"
              :placeholder="currentMode === 'chat' 
                ? 'Напишите сообщение...' 
                : documentsCount === 0 
                  ? 'Сначала загрузите документы в настройках...'
                  : 'Задайте вопрос по документам...'"
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
            :disabled="!currentMessage.trim() || isTyping || (currentMode === 'rag' && documentsCount === 0)"
            class="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { 
  Bot, Menu, X, MessageSquare, FileText, Upload, Send, Loader2 
} from 'lucide-vue-next'
import { ragApi, type SimpleChatMessage, type SearchResult } from '@/api/ragApi'
import LLMSettings from '@/components/settings/LLMSettings.vue'
import DocumentManager from '@/components/documents/DocumentManager.vue'

// Интерфейс для сообщений UI
interface UIMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: SearchResult[]
}

// Реактивные данные
const sidebarOpen = ref(true)
const currentMode = ref<'chat' | 'rag'>('chat')
const activeSettingsTab = ref<'llm' | 'documents'>('llm')

const messages = ref<UIMessage[]>([])
const currentMessage = ref('')
const isTyping = ref(false)

const llmStatus = ref<any>(null)
const documentsCount = ref(0)
const embeddingsModel = ref('')

// Refs
const messageInput = ref<HTMLTextAreaElement>()
const chatContainer = ref<HTMLElement>()

// Вычисляемые свойства
const currentExamples = computed(() => {
  if (currentMode.value === 'chat') {
    return [
      'Привет! Как дела?',
      'Расскажи интересный факт',
      'Помоги с программированием',
      'Что такое машинное обучение?'
    ]
  } else {
    return [
      'О чем этот документ?',
      'Какие основные темы рассматриваются?',
      'Есть ли примеры кода?',
      'Какие выводы можно сделать?'
    ]
  }
})

// Методы
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const clearChat = () => {
  messages.value = []
}

const loadSystemStatus = async () => {
  try {
    const [llmStatusResponse, documentsResponse] = await Promise.all([
      ragApi.getLLMStatus(),
      ragApi.getDocuments()
    ])
    
    llmStatus.value = llmStatusResponse
    documentsCount.value = documentsResponse.total_documents
    embeddingsModel.value = 'rubert-tiny2' // Можно получить из API
  } catch (error) {
    console.error('Failed to load system status:', error)
  }
}

const sendMessage = async (messageText?: string) => {
  const text = messageText || currentMessage.value.trim()
  if (!text || isTyping.value) return

  // Добавляем сообщение пользователя
  const userMessage: UIMessage = {
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
    let response
    
    if (currentMode.value === 'chat') {
      // Простой чат
      const history: SimpleChatMessage[] = messages.value
        .slice(-10)
        .map(msg => ({
          role: msg.type === 'user' ? 'user' : 'assistant',
          content: msg.content
        }))

      response = await ragApi.simpleChat(text, history)
      
      const assistantMessage: UIMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.response,
        timestamp: new Date()
      }
      messages.value.push(assistantMessage)
      
    } else {
      // RAG чат
      response = await ragApi.chatWithDocuments(text)
      
      const assistantMessage: UIMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        sources: response.sources
      }
      messages.value.push(assistantMessage)
    }

  } catch (error) {
    console.error('Chat failed:', error)
    
    const errorMessage: UIMessage = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: 'Извините, произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.',
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

const formatTime = (date: Date): string => {
  return date.toLocaleTimeString('ru-RU', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const onLLMSettingsApplied = async () => {
  await loadSystemStatus()
}

const onDocumentsUpdated = async () => {
  await loadSystemStatus()
}

const onDocumentUploaded = async () => {
  await loadSystemStatus()
}

// Инициализация
onMounted(async () => {
  await loadSystemStatus()
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