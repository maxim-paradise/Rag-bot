<template>
  <div class="flex justify-center items-center w-full">
    <div class="relative w-full">
      <!-- Main input container -->
      <div 
        class="relative flex items-center rounded-2xl px-6 py-4 shadow-lg w-full"
        style="background-color: hsl(var(--muted))"
      >
        <!-- Left plus icon -->
        <div class="flex-shrink-0 mr-3">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: hsl(var(--foreground))">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
        </div>

        <!-- Textarea field -->
        <textarea
          v-model="text"
          rows="1"
          placeholder="Ask anything"
          class="flex-1 bg-transparent outline-none resize-none text-xl overflow-hidden w-full"
          style="color: hsl(var(--foreground));"
          @input="autoResize"
          @keydown="handleKeyDown"
        ></textarea>

        <!-- Right icons -->
        <div class="flex-shrink-0 ml-3 rounded-full p-2 flex items-center space-x-2" style="background-color: hsl(var(--secondary))">
          <!-- Microphone icon -->
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: hsl(var(--foreground))">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path>
          </svg>
          <!-- Sound waves -->
          <div class="flex items-center space-x-1">
            <div class="w-0.5 h-3 rounded-full" style="background-color: hsl(var(--foreground))"></div>
            <div class="w-0.5 h-4 rounded-full" style="background-color: hsl(var(--foreground))"></div>
            <div class="w-0.5 h-2 rounded-full" style="background-color: hsl(var(--foreground))"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
  send: [message: string]
}>()

const text = ref("");

const autoResize = (e: Event) => {
  const el = e.target as HTMLTextAreaElement;
  el.style.height = "auto";
  el.style.height = `${el.scrollHeight}px`;
};

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    if (event.shiftKey) {
      // Shift+Enter - новая строка (стандартное поведение)
      return;
    } else {
      // Enter - отправить сообщение
      event.preventDefault();
      sendMessage();
    }
  }
};

const sendMessage = () => {
  if (text.value.trim()) {
    emit('send', text.value.trim());
    text.value = '';
    // Сброс высоты textarea
    const textarea = document.querySelector('textarea') as HTMLTextAreaElement;
    if (textarea) {
      textarea.style.height = 'auto';
    }
  }
};
</script>

<style scoped>
textarea::placeholder {
  color: hsl(var(--muted-foreground));
}
</style>
