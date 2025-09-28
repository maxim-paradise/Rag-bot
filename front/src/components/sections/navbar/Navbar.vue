<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'
import { ref } from 'vue'
import type { HTMLAttributes } from 'vue'

type NavbarProps = {
  class?: HTMLAttributes['class']
  position?: 'fixed' | 'sticky' | 'relative'
  size?: 'sm' | 'default' | 'lg'
}

const props = withDefaults(defineProps<NavbarProps>(), {
  position: 'sticky',
  size: 'default'
})

const navbarClasses = `flex h-16 items-center border-b border-border/50 dark:border-border/30 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 ${props.position === 'fixed' ? 'fixed top-0 w-full z-50' : props.position === 'sticky' ? 'sticky top-0 z-50' : 'relative'}`

const isDropdownOpen = ref(false)
const selectedModel = ref('GPT-4')

const models = [
  'GPT-4',
  'GPT-3.5 Turbo',
  'Claude 3',
  'Gemini Pro'
]

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const selectModel = (model: string) => {
  selectedModel.value = model
  isDropdownOpen.value = false
}
</script>

<template>
  <header :class="[navbarClasses, props.class]">
    <div class="flex h-full items-center px-4">
      <div class="relative">
        <button
          @click="toggleDropdown"
          class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-accent transition-colors"
        >
          <span class="text-lg font-bold">AI RAG</span>
          <ChevronDown class="h-4 w-4" :class="{ 'rotate-180': isDropdownOpen }" />
        </button>
        
        <!-- Dropdown Menu -->
        <div
          v-if="isDropdownOpen"
          class="absolute top-full left-0 mt-1 w-48 rounded-md border bg-background shadow-lg z-50"
        >
          <div class="py-1">
            <button
              v-for="model in models"
              :key="model"
              @click="selectModel(model)"
              class="w-full text-left px-3 py-2 text-sm hover:bg-accent transition-colors"
              :class="{ 'bg-accent': selectedModel === model }"
            >
              {{ model }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Overlay to close dropdown -->
    <div
      v-if="isDropdownOpen"
      class="fixed inset-0 z-40"
      @click="isDropdownOpen = false"
    />
  </header>
</template> 