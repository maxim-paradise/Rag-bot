<template>
  <div
    v-if="open"
    class="fixed top-4 right-4 z-50 flex w-full max-w-sm items-center space-x-4 divide-x divide-border rounded-md border bg-background p-4 shadow-lg"
    role="alert"
  >
    <div class="flex-1">
      <div class="text-sm font-medium">{{ title }}</div>
      <div v-if="description" class="text-sm text-muted-foreground">{{ description }}</div>
    </div>
    <button
      v-if="showClose"
      @click="close"
      class="ml-4 text-muted-foreground hover:text-foreground"
      type="button"
    >
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Props {
  title: string
  description?: string
  duration?: number
  showClose?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  duration: 5000,
  showClose: true
})

const emit = defineEmits<{
  close: []
}>()

const open = ref(false)

const close = () => {
  open.value = false
  emit('close')
}

onMounted(() => {
  open.value = true
  if (props.duration > 0) {
    setTimeout(() => {
      close()
    }, props.duration)
  }
})
</script>