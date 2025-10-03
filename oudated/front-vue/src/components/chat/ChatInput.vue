<template>
  <div class="border-t bg-background p-6">
    <form @submit.prevent="handleSubmit" class="flex gap-4">
      <div class="relative flex-1">
        <textarea
          ref="textareaRef"
          v-model="message"
          :disabled="isLoading"
          placeholder="Напишите сообщение..."
          class="min-h-[60px] max-h-40 w-full resize-none rounded-xl border border-input bg-background px-6 py-4 text-lg placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          @keydown="handleKeyDown"
          @input="adjustHeight"
        />
      </div>
      
      <button
        type="submit"
        :disabled="!message.trim() || isLoading"
        class="flex h-16 w-16 items-center justify-center rounded-xl bg-primary text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <component :is="isLoading ? LoaderIcon : SendIcon" class="h-6 w-6" :class="{ 'animate-spin': isLoading }" />
      </button>
    </form>
    
    <div class="mt-2 text-xs text-muted-foreground">
      Нажмите Enter для отправки, Shift+Enter для новой строки
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { Send, Loader } from 'lucide-vue-next'

const emit = defineEmits<{
  send: [message: string]
}>()

const message = ref('')
const isLoading = ref(false)
const textareaRef = ref<HTMLTextAreaElement>()

const SendIcon = Send
const LoaderIcon = Loader

const handleSubmit = () => {
  if (!message.value.trim() || isLoading.value) return
  
  emit('send', message.value.trim())
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

const setLoading = (loading: boolean) => {
  isLoading.value = loading
}

defineExpose({
  setLoading
})
</script>