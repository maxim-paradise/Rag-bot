<template>
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    @click="closeSettings"
  >
    <div 
      class="w-full max-w-md rounded-lg border bg-background p-6 shadow-lg"
      @click.stop
    >
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold">Настройки</h2>
        <button
          @click="closeSettings"
          class="flex h-8 w-8 items-center justify-center rounded-md hover:bg-accent transition-colors"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
      
      <div class="space-y-6">
        <!-- Dark Mode Toggle -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Темная тема</label>
          <div class="flex items-center justify-between">
            <span class="text-sm text-muted-foreground">Переключить темную тему</span>
            <DarkMode />
          </div>
        </div>
        
        <!-- Theme Settings -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Цветовая схема</label>
          <div class="grid grid-cols-3 gap-2">
            <button 
              v-for="color in colorOptions"
              :key="color"
              class="relative flex items-center justify-center rounded-md border p-2 transition-colors hover:bg-accent"
              :class="{ 'border-primary bg-accent': selectedColor === color }"
              @click="selectedColor = color; updateTheme()"
            >
              <span 
                class="absolute left-2 h-3 w-3 rounded-full"
                :class="`bg-${color}-500`"
              />
              <span class="text-xs capitalize">{{ color }}</span>
            </button>
          </div>
        </div>
        
        <!-- Font Settings -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Шрифт</label>
          <select 
            v-model="selectedFont"
            class="w-full rounded-md border bg-background px-3 py-2 text-sm"
            @change="updateTheme"
          >
            <option 
              v-for="font in fontOptions"
              :key="font"
              :value="font"
              :style="{ fontFamily: font }"
            >
              {{ font }}
            </option>
          </select>
        </div>
        
        <!-- Radius Settings -->
        <div class="space-y-2">
          <label class="text-sm font-medium">Скругление углов</label>
          <div class="grid grid-cols-5 gap-2">
            <button
              v-for="radius in radiusOptions"
              :key="radius"
              class="rounded-md border p-2 text-xs transition-colors hover:bg-accent"
              :class="{ 'border-primary bg-accent': selectedRadius === radius }"
              @click="selectedRadius = radius; updateTheme()"
            >
              {{ formatRadius(radius) }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X } from 'lucide-vue-next'
import DarkMode from '@/components/darkMode/DarkMode.vue'
import { initializeTheme, currentTheme, applyThemeClass, generateTailwindStyles } from '@/components/theming/themeManager'
import { useFont } from '@/composables/useFont'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const colorOptions = ['red', 'rose', 'orange', 'green', 'blue', 'violet']
const fontOptions = [
  'Nunito', 'Inter', 'Roboto', 'Lato', 'Lexend', 'Urbanist',
  'Kanit', 'Fira Sans', 'Karla', 'Prompt', 'Saira', 'Geologica', 
  'Bai Jamjuree', 'Niramit', 'Livvic', 'Exo', 'K2D', 'Jura', 
  'Philosopher', 'Montserrat', 'Open Sans', 'Rubik', 'Oswald',
  'Work Sans', 'Mulish', 'Barlow', 'Heebo', 'Titillium Web', 
  'Libre Franklin', 'Josefin Sans', 'Jost', 'Outfit', 'Figtree', 
  'Overpass', 'Chivo', 'Alegreya Sans', 'Fahkwang'
]
const radiusOptions = ['0', '0.3em', '0.5em', '0.75em', '1em']

const selectedFont = ref(
  JSON.parse(localStorage.getItem('currentState') || '{}')?.sceleton?.config?.theme?.fontFamily?.sans?.[0] || 'Nunito'
)
const selectedColor = ref(currentTheme.value || 'green')
const selectedRadius = ref(JSON.parse(localStorage.getItem('currentState') || '{}')?.sceleton?.radius || '0.5rem')

const { loadFont, updateFontLink } = useFont()

const formatRadius = (value: string) => value.replace('em', '')

const updateTheme = async () => {
  const currentState = JSON.parse(localStorage.getItem('currentState') || '{}')
  
  if (!currentState.sceleton) currentState.sceleton = {}
  if (!currentState.sceleton.config) currentState.sceleton.config = {}
  
  // Загружаем базовую конфигурацию
  const defaultConfig = {
    darkMode: "class",
    theme: {
      fontFamily: {
        sans: [selectedFont.value, "sans-serif"]
      },
      container: {
        center: true,
        padding: "2rem"
      },
      extend: {
        colors: {
          border: "hsl(var(--border))",
          input: "hsl(var(--input))",
          ring: "hsl(var(--ring))",
          background: "hsl(var(--background))",
          foreground: "hsl(var(--foreground))",
          primary: {
            DEFAULT: "hsl(var(--primary))",
            foreground: "hsl(var(--primary-foreground))"
          },
          secondary: {
            DEFAULT: "hsl(var(--secondary))",
            foreground: "hsl(var(--secondary-foreground))"
          },
          destructive: {
            DEFAULT: "hsl(var(--destructive))",
            foreground: "hsl(var(--destructive-foreground))"
          },
          muted: {
            DEFAULT: "hsl(var(--muted))",
            foreground: "hsl(var(--muted-foreground))"
          },
          accent: {
            DEFAULT: "hsl(var(--accent))",
            foreground: "hsl(var(--accent-foreground))"
          },
          popover: {
            DEFAULT: "hsl(var(--popover))",
            foreground: "hsl(var(--popover-foreground))"
          },
          card: {
            DEFAULT: "hsl(var(--card))",
            foreground: "hsl(var(--card-foreground))"
          }
        },
        borderRadius: {
          xl: "calc(var(--radius) + 4px)",
          lg: "var(--radius)",
          md: "calc(var(--radius) - 2px)",
          sm: "calc(var(--radius) - 4px)"
        }
      }
    }
  }

  // Обновляем только шрифт в конфигурации
  currentState.sceleton.config = defaultConfig
  currentState.sceleton.config.theme.fontFamily.sans = [selectedFont.value, "sans-serif"]
  
  currentTheme.value = selectedColor.value
  currentState.sceleton.theme = selectedColor.value
  currentState.sceleton.radius = selectedRadius.value
  currentState.sceleton.tailwindStyles = generateTailwindStyles(selectedColor.value, selectedRadius.value)
  
  updateFontLink(selectedFont.value)
  await loadFont(selectedFont.value)
  
  document.documentElement.style.setProperty('--radius', selectedRadius.value)
  
  const serializedState = JSON.stringify(currentState, null, 2)
  localStorage.setItem('currentState', serializedState)
  
  applyThemeClass(selectedColor.value)
}

const closeSettings = () => {
  emit('close')
}

onMounted(() => {
  initializeTheme()
  if (currentTheme.value && currentTheme.value !== selectedColor.value) {
    selectedColor.value = currentTheme.value
    updateTheme()
  }
})
</script>