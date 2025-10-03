<template>
  <div class="h-[calc(100vh-4rem)] bg-background flex flex-col">
    <!-- Заголовок -->
    <div class="p-4 border-b border-border bg-card">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold text-foreground flex items-center gap-2">
            <Bot class="w-5 h-5" />
            AI Чат
          </h1>
          <p class="text-sm text-muted-foreground">
            Общайтесь с искусственным интеллектом
          </p>
        </div>
        
        <!-- Статус LLM и настройки -->
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <div :class="[
              'w-2 h-2 rounded-full',
              llmStatus === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
            ]" />
            <span class="text-xs text-muted-foreground">
              {{ llmStatus === 'ready' ? 'LLM готов' : 'Режим заглушки' }}
            </span>
          </div>
          
          <button
            @click="showSettings = !showSettings"
            class="p-1 hover:bg-muted rounded transition-colors"
            title="Настройки LLM"
          >
            <Settings class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>

    <!-- Сообщения чата -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="chatContainer">
      <div v-if="messages.length === 0" class="text-center py-12">
        <Bot class="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
        <h3 class="text-lg font-medium mb-2">Начните разговор</h3>
        <p class="text-muted-foreground mb-4">
          Задайте любой вопрос или просто поздоровайтесь
        </p>
        <div class="flex flex-wrap gap-2 justify-center">
          <button
            v-for="example in exampleMessages"
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
              {{ message.type === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="text-xs text-muted-foreground">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
          
          <div class="prose prose-sm max-w-none">
            <p class="whitespace-pre-wrap">{{ message.content }}</p>
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
            :disabled="isTyping"
            placeholder="Напишите сообщение..."
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
          :disabled="!currentMessage.trim() || isTyping"
          class="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send class="w-4 h-4" />
        </button>
      </div>
      
      <!-- Информация о статусе -->
      <div class="text-xs text-muted-foreground mt-2 flex items-center gap-2">
        <Info class="w-3 h-3" />
        {{ llmStatus === 'ready' 
          ? 'Подключен к языковой модели' 
          : 'Работает в режиме заглушки. Настройте API ключи для полноценного общения.' 
        }}
      </div>
    </div>

    <!-- Панель настроек LLM -->
    <div v-if="showSettings" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-card rounded-lg shadow-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold">Настройки LLM</h2>
            <button
              @click="showSettings = false"
              class="p-2 hover:bg-muted rounded-lg transition-colors"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <LLMSettings @settings-applied="onSettingsApplied" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Bot, Send, Loader2, Info, Settings, X } from 'lucide-vue-next'
import { ragApi, type SimpleChatMessage } from '@/api/ragApi'
import LLMSettings from '@/components/settings/LLMSettings.vue'

// Интерфейс для сообщений UI
interface UIMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// Реактивные данные
const messages = ref<UIMessage[]>([])
const currentMessage = ref('')
const isTyping = ref(false)
const llmStatus = ref<'ready' | 'fallback'>('fallback')
const showSettings = ref(false)

// Refs
const messageInput = ref<HTMLTextAreaElement>()
const chatContainer = ref<HTMLElement>()

// Примеры сообщений
const exampleMessages = [
  'Привет! Как дела?',
  'Расскажи интересный факт',
  'Помоги с программированием',
  'Что такое машинное обучение?',
  'Расскажи анекдот'
]

// Методы
const checkLLMStatus = async () => {
  try {
    const status = await ragApi.getLLMStatus()
    llmStatus.value = status.status === 'ready' ? 'ready' : 'fallback'
  } catch (error) {
    console.error('Failed to check LLM status:', error)
    llmStatus.value = 'fallback'
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
    // Формируем историю для API
    const history: SimpleChatMessage[] = messages.value
      .slice(-10) // Берем последние 10 сообщений
      .map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }))

    const response = await ragApi.simpleChat(text, history)
    
    // Добавляем ответ ассистента
    const assistantMessage: UIMessage = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: response.response,
      timestamp: new Date()
    }
    messages.value.push(assistantMessage)

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

const onSettingsApplied = async () => {
  // Обновляем статус LLM после применения настроек
  await checkLLMStatus()
  showSettings.value = false
}

// Инициализация
onMounted(async () => {
  await checkLLMStatus()
})
</script>

<style scoped>
.prose p {
  margin: 0;
}
</style>