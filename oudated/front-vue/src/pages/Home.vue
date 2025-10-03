<template>
  <div class="flex h-screen bg-background relative">
    <!-- Mobile Overlay -->
    <div 
      v-if="isSidebarOpen && windowWidth < 768"
      class="fixed inset-0 bg-black/50 z-40 md:hidden"
      @click="toggleSidebar"
    />
    
    <!-- Sidebar -->
    <div 
      class="transition-all duration-300 ease-in-out overflow-hidden relative z-50"
      :class="[
        isSidebarOpen ? 'w-64' : 'w-16',
        windowWidth < 768 ? 'fixed left-0 top-0 h-full' : 'relative'
      ]"
    >
      <div class="h-full">
        <ChatSidebar 
          v-if="isSidebarOpen"
          :is-sidebar-open="isSidebarOpen"
          @select-chat="handleSelectChat"
          @new-chat="handleNewChat"
          @toggle-sidebar="toggleSidebar"
          @toggle-settings="toggleSettings"
        />
        <ChatSidebarCollapsed 
          v-else
          @toggle-sidebar="toggleSidebar"
          @new-chat="handleNewChat"
          @toggle-settings="toggleSettings"
        />
      </div>
    </div>
    
    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col">
      <Navbar />
      <ChatContainer />
    </div>
    
    <!-- Settings Panel -->
    <SettingsPanel 
      :is-open="isSettingsOpen"
      @close="closeSettings"
    />

    <!-- AI Settings Panel -->
    <AISettingsPanel 
      :is-open="isAISettingsOpen"
      @close="closeAISettings"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChatContainer } from '@/components/chat'

const router = useRouter()
import ChatSidebar from '@/components/chat/ChatSidebar/index.vue'
import ChatSidebarCollapsed from '@/components/chat/ChatSidebarCollapsed.vue'
import Navbar from '@/components/sections/navbar/Navbar.vue'
import SettingsPanel from '@/components/settings/SettingsPanel.vue'
import AISettingsPanel from '@/components/settings/AISettingsPanel.vue'

// Определяем начальное состояние сайдбара (скрыт на мобильных устройствах)
const isSidebarOpen = ref(window.innerWidth >= 768)
const windowWidth = ref(window.innerWidth)
const isSettingsOpen = ref(false)
const isAISettingsOpen = ref(false)

// Обработчик изменения размера окна
const handleResize = () => {
  windowWidth.value = window.innerWidth
  // На мобильных устройствах автоматически закрываем сайдбар при изменении размера
  if (window.innerWidth < 768 && isSidebarOpen.value) {
    isSidebarOpen.value = false
  }
}

// Загружаем состояние сайдбара из localStorage
onMounted(() => {
  const savedState = localStorage.getItem('sidebarOpen')
  if (savedState !== null) {
    isSidebarOpen.value = JSON.parse(savedState)
  } else {
    // Если нет сохраненного состояния, используем адаптивную логику
    isSidebarOpen.value = window.innerWidth >= 768
  }
  
  // Добавляем обработчик изменения размера окна
  window.addEventListener('resize', handleResize)
  
  // Добавляем обработчики горячих клавиш
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('keydown', handleKeyDown)
})

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
  // Сохраняем состояние в localStorage
  localStorage.setItem('sidebarOpen', JSON.stringify(isSidebarOpen.value))
}

const handleSelectChat = (chatId: string) => {
  console.log('Selected chat:', chatId)
  // На мобильных устройствах закрываем сайдбар после выбора чата
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false
  }
}

const handleNewChat = () => {
  console.log('New chat created')
  // На мобильных устройствах закрываем сайдбар после создания нового чата
  if (window.innerWidth < 768) {
    isSidebarOpen.value = false
  }
}

const toggleSettings = () => {
  isSettingsOpen.value = !isSettingsOpen.value
}

const closeSettings = () => {
  isSettingsOpen.value = false
}

const closeAISettings = () => {
  isAISettingsOpen.value = false
}

const handleKeyDown = (event: KeyboardEvent) => {
  // Ctrl+Shift+N - новый чат
  if (event.ctrlKey && event.shiftKey && event.key === 'N') {
    event.preventDefault()
    handleNewChat()
  }
  
  // Ctrl+K - поиск чатов
  if (event.ctrlKey && event.key === 'k') {
    event.preventDefault()
    // Здесь можно добавить функциональность поиска
    console.log('Search chats triggered')
  }
}
</script>