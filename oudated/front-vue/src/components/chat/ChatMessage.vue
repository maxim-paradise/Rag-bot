<template>
  <div class="group relative flex w-full items-start gap-4 p-4">
    <div class="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background shadow">
      <component :is="message.role === 'user' ? UserIcon : BotIcon" class="h-4 w-4" />
    </div>
    
    <div class="flex-1 space-y-2 overflow-hidden">
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium">
          {{ message.role === 'user' ? 'Вы' : 'AI Assistant' }}
        </span>
        <span class="text-xs text-muted-foreground">
          {{ formatTime(message.timestamp) }}
        </span>
      </div>
      
      <div class="prose prose-sm max-w-none dark:prose-invert">
        <div v-if="message.role === 'assistant'" class="whitespace-pre-wrap">{{ message.content }}</div>
        <div v-else class="whitespace-pre-wrap">{{ message.content }}</div>
      </div>
      
      <div v-if="message.role === 'assistant' && !message.isComplete" class="flex items-center gap-2">
        <div class="flex space-x-1">
          <div class="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.3s]"></div>
          <div class="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.15s]"></div>
          <div class="h-2 w-2 animate-bounce rounded-full bg-primary"></div>
        </div>
        <span class="text-xs text-muted-foreground">AI печатает...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { User, Bot } from 'lucide-vue-next'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isComplete?: boolean
}

defineProps<{
  message: ChatMessage
}>()

const UserIcon = User
const BotIcon = Bot

const formatTime = (date: Date) => {
  return new Intl.DateTimeFormat('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>