<template>
  <div class="flex h-full w-16 flex-col border-r bg-background">
    <!-- Logo/Menu Toggle Button -->
    <div class="flex flex-col items-center p-4">
      <button
        @click="toggleSidebar"
        class="group flex h-8 w-8 items-center justify-center rounded-md hover:bg-accent transition-colors"
        title="Открыть боковую панель"
      >
        <!-- Логотип по умолчанию -->
        <Bot class="h-6 w-6 text-foreground group-hover:hidden" />
        <!-- Иконка меню при наведении -->
        <Menu class="h-6 w-6 text-foreground hidden group-hover:block" />
      </button>
    </div>
    
    <!-- Navigation Icons -->
    <div class="flex flex-1 flex-col items-center gap-2 p-3">
      <button
        @click="createNewChat"
        class="group flex h-8 w-8 items-center justify-center rounded-md hover:bg-accent/50 transition-all duration-200 hover:shadow-sm"
        title="New chat (Ctrl+Shift+N)"
      >
        <div class="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10 group-hover:bg-primary/20 transition-colors">
          <Plus class="h-3 w-3 text-primary" />
        </div>
      </button>
      
      <button
        class="group flex h-8 w-8 items-center justify-center rounded-md hover:bg-accent/50 transition-all duration-200 hover:shadow-sm"
        title="Search chats (Ctrl+K)"
      >
        <div class="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10 group-hover:bg-primary/20 transition-colors">
          <Search class="h-3 w-3 text-primary" />
        </div>
      </button>
    </div>
    
    <!-- Settings Buttons -->
    <div class="flex flex-col items-center p-3 space-y-2">
      <button
        @click="toggleAISettings"
        class="flex h-10 w-10 items-center justify-center rounded-lg hover:bg-accent transition-colors"
        title="AI Настройки"
      >
        <Bot class="h-5 w-5 text-foreground" />
      </button>
      <button
        @click="toggleSettings"
        class="flex h-10 w-10 items-center justify-center rounded-lg hover:bg-accent transition-colors"
        title="Настройки темы"
      >
        <Settings class="h-5 w-5 text-foreground" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Menu, Search, Image, Bot, Settings, Plus } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const emit = defineEmits<{
  toggleSidebar: []
  newChat: []
  toggleSettings: []
}>()

const toggleSidebar = () => {
  console.log('Toggle sidebar clicked in ChatSidebarCollapsed')
  emit('toggleSidebar')
}

const createNewChat = () => {
  emit('newChat')
}

const toggleSettings = () => {
  emit('toggleSettings')
}

const toggleAISettings = () => {
  router.push('/ai-settings')
}
</script>