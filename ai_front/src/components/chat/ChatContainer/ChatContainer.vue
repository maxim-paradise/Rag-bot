<template>
  <div class="flex h-full flex-col">
    <!-- Empty Chat State - Centered Input with Lamp Effect -->
    <div v-if="messages.length === 0" class="flex-1 relative">
      <!-- Dark theme with LampEffect -->
      <div v-if="isDarkMode" class="h-full relative">
        <LampEffect class="h-full">
          <div class="text-center space-y-8 w-full -translate-y-16 px-4">
            <div>
              <h2 class="text-2xl font-semibold mb-2">How can I help, Maxim?</h2>
            </div>
            
            <div class="w-full max-w-2xl mx-auto">
              <UserArea @send="handleSendMessage" />
            </div>
          </div>
        </LampEffect>
      </div>
      
      <!-- Light theme without LampEffect -->
      <div v-else class="h-full flex items-center justify-center bg-background">
        <div class="text-center space-y-8 w-full px-4">
          <div>
            <h2 class="text-2xl font-semibold mb-2">How can I help, Maxim?</h2>
          </div>
          
          <div class="w-full max-w-2xl mx-auto">
            <UserArea @send="handleSendMessage" />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Chat with Messages -->
    <div v-else class="flex h-full flex-col">
      <!-- Messages Area -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto">
        <div class="space-y-0">
          <ChatMessage
            v-for="message in messages"
            :key="message.id"
            :message="message"
          />
        </div>
      </div>
      
      <!-- Chat Input at Bottom -->
      <div class="w-full max-w-2xl mb-12 mx-auto px-4">
        <UserArea @send="handleSendMessage" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch, onMounted } from 'vue'
import { Send, Loader } from 'lucide-vue-next'
import ChatMessage from '../ChatMessage.vue'
import LampEffect from '@/components/global/LampEffect/index.vue'
import { useChatAPI } from '@/composables/useChatAPI'
import UserArea from './layout/user-area.vue'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isComplete?: boolean
}

const messages = ref<ChatMessage[]>([])
const messagesContainer = ref<HTMLElement>()
const textareaRef = ref<HTMLTextAreaElement>()
const message = ref('')
const { sendMessage, isLoading } = useChatAPI()

// Dark mode detection
const isDarkMode = ref(false)

const checkDarkMode = () => {
  isDarkMode.value = document.documentElement.classList.contains('dark')
}

onMounted(() => {
  checkDarkMode()
  
  // Watch for dark mode changes
  const observer = new MutationObserver(() => {
    checkDarkMode()
  })
  
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

const SendIcon = Send
const LoaderIcon = Loader

const handleSendMessage = async (content: string) => {
  // Добавляем сообщение пользователя
  const userMessage: ChatMessage = {
    id: Date.now().toString(),
    role: 'user',
    content,
    timestamp: new Date(),
    isComplete: true
  }
  
  messages.value.push(userMessage)
  
  // Добавляем пустое сообщение ассистента
  const assistantMessage: ChatMessage = {
    id: (Date.now() + 1).toString(),
    role: 'assistant',
    content: '',
    timestamp: new Date(),
    isComplete: false
  }
  
  messages.value.push(assistantMessage)
  
  // Прокручиваем к последнему сообщению
  await nextTick()
  scrollToBottom()
  
  // Отправляем запрос к API
  try {
    const response = await sendMessage(content)
    
    // Обновляем сообщение ассистента
    const lastMessage = messages.value[messages.value.length - 1]
    if (lastMessage && lastMessage.role === 'assistant') {
      lastMessage.content = response
      lastMessage.isComplete = true
    }
  } catch (error) {
    console.error('Ошибка при отправке сообщения:', error)
    
    // Обновляем сообщение ассистента с ошибкой
    const lastMessage = messages.value[messages.value.length - 1]
    if (lastMessage && lastMessage.role === 'assistant') {
      lastMessage.content = 'Извините, произошла ошибка. Попробуйте еще раз.'
      lastMessage.isComplete = true
    }
  } finally {
    await nextTick()
    scrollToBottom()
  }
}

const clearChat = () => {
  messages.value = []
}

// Functions for centered input
const handleSubmit = () => {
  if (!message.value.trim() || isLoading.value) return
  
  handleSendMessage(message.value.trim())
  message.value = ''
  adjustHeight()
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSubmit()
  }
}

const adjustHeight = async () => {
  await nextTick()
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = `${Math.min(textareaRef.value.scrollHeight, 128)}px`
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Автоматическая прокрутка при добавлении новых сообщений
watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })
</script>