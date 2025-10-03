<template>
  <div class="flex h-full w-64 flex-col border-r bg-background">
    <!-- Sidebar Header -->
    <div class="flex items-center justify-between border-b p-2">
      <!-- Left side - Logo/Icon -->
      <div class="flex items-center gap-2">
        <div class="flex h-8 w-8 items-center justify-center rounded-md">
          <Bot class="h-4 w-4" />
        </div>
      </div>
      
      <!-- Right side - Close button -->
      <button
        @click="toggleSidebar"
        class="flex h-8 w-8 items-center justify-center rounded-md hover:bg-accent transition-colors"
        title="Закрыть боковую панель"
      >
        <X class="h-4 w-4" />
      </button>
    </div>
    
    <!-- Chat History -->
    <div class="flex-1 overflow-y-auto p-4">
      <!-- New Chat Button -->
      <button
        @click="createNewChat"
        class="group w-full rounded-md p-2 text-left text-xs transition-all duration-200 hover:bg-accent/50 hover:border-accent/50 border border-transparent hover:shadow-sm mb-2"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10 group-hover:bg-primary/20 transition-colors">
              <Plus class="h-3 w-3 text-primary" />
            </div>
            <span class="font-medium text-foreground">New chat</span>
          </div>
          <div class="flex items-center gap-1 text-xs text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
            <kbd class="px-1 py-0.5 text-xs bg-muted rounded border">Ctrl</kbd>
            <kbd class="px-1 py-0.5 text-xs bg-muted rounded border">Shift</kbd>
            <kbd class="px-1 py-0.5 text-xs bg-muted rounded border">N</kbd>
          </div>
        </div>
      </button>
      
      <!-- Search Chats Button -->
      <button
        class="group w-full rounded-md p-2 text-left text-xs transition-all duration-200 hover:bg-accent/50 hover:border-accent/50 border border-transparent hover:shadow-sm mb-2"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10 group-hover:bg-primary/20 transition-colors">
              <Search class="h-3 w-3 text-primary" />
            </div>
            <span class="font-medium text-foreground">Search chats</span>
          </div>
          <div class="flex items-center gap-1 text-xs text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
            <kbd class="px-1 py-0.5 text-xs bg-muted rounded border">Ctrl</kbd>
            <kbd class="px-1 py-0.5 text-xs bg-muted rounded border">K</kbd>
          </div>
        </div>
      </button>
      
      <div v-if="chatHistory.length === 0" class="text-center py-8">
        <MessageCircle class="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
        <p class="text-sm text-muted-foreground">Нет сохраненных чатов</p>
      </div>
      
      <div v-else class="space-y-1">
        <button
          v-for="chat in chatHistory"
          :key="chat.id"
          @click="selectChat(chat.id)"
          class="w-full rounded-md p-3 text-left text-sm hover:bg-accent transition-colors"
          :class="{ 'bg-accent': selectedChatId === chat.id }"
        >
          <div class="font-medium truncate">{{ chat.title }}</div>
          <div class="text-xs text-muted-foreground">{{ formatDate(chat.updatedAt) }}</div>
        </button>
      </div>
    </div>
    
    <!-- Sidebar Footer -->
    <div class="border-t p-4 space-y-2">
      <button
        @click="toggleAISettings"
        class="flex w-full items-center gap-2 rounded-md p-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      >
        <Bot class="h-4 w-4" />
        AI Настройки
      </button>
      <button
        @click="toggleSettings"
        class="flex w-full items-center gap-2 rounded-md p-2 text-sm text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      >
        <Settings class="h-4 w-4" />
        Настройки темы
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, MessageCircle, X, Bot, Settings, Search } from 'lucide-vue-next'

const router = useRouter()

interface ChatHistoryItem {
  id: string
  title: string
  updatedAt: Date
  messageCount: number
}

const emit = defineEmits<{
  selectChat: [chatId: string]
  newChat: []
  toggleSidebar: []
  toggleSettings: []
}>()

const props = defineProps<{
  isSidebarOpen?: boolean
}>()

const selectedChatId = ref<string | null>(null)
const chatHistory = ref<ChatHistoryItem[]>([
  {
    id: '1',
    title: 'Как работает машинное обучение?',
    updatedAt: new Date(Date.now() - 1000 * 60 * 30), // 30 минут назад
    messageCount: 4
  },
  {
    id: '2',
    title: 'Объясни квантовую физику',
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 часа назад
    messageCount: 6
  },
  {
    id: '3',
    title: 'Помоги с программированием',
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 день назад
    messageCount: 8
  }
])

const createNewChat = () => {
  const newChat: ChatHistoryItem = {
    id: Date.now().toString(),
    title: 'Новый чат',
    updatedAt: new Date(),
    messageCount: 0
  }
  
  chatHistory.value.unshift(newChat)
  selectedChatId.value = newChat.id
  emit('newChat')
}

const toggleSidebar = () => {
  emit('toggleSidebar')
}

const toggleSettings = () => {
  emit('toggleSettings')
}

const toggleAISettings = () => {
  router.push('/ai-settings')
}

const selectChat = (chatId: string) => {
  selectedChatId.value = chatId
  emit('selectChat', chatId)
}


const formatDate = (date: Date) => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 60) {
    return `${minutes} мин назад`
  } else if (hours < 24) {
    return `${hours} ч назад`
  } else {
    return `${days} дн назад`
  }
}
</script>