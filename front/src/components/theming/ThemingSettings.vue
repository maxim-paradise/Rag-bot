<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Palette } from 'lucide-vue-next'
import { initializeTheme, currentTheme, applyThemeClass, generateTailwindStyles } from './themeManager'
import { useFont } from '@/composables/useFont'

const formatRadius = (value: string) => value.replace('em', '')

const isOpen = ref(false)

const sheetContent = {
  header: {
    title: 'Theme Settings',
    description: 'Manage application appearance'
  },
  theme: {
    title: 'Theme Settings',
    sections: [
      {
        label: 'Color Scheme',
        type: 'colors',
        options: ['red', 'rose', 'orange', 'green', 'blue', 'violet']
      },
      {
        label: 'Corner Radius',
        type: 'radius',
        options: ['0', '0.3em', '0.5em', '0.75em', '1em']
      },
      {
        label: 'Font Family',
        type: 'font',
        options: [
          'Nunito', 'Inter', 'Roboto', 'Lato', 'Lexend', 'Urbanist',
          'Kanit', 'Fira Sans', 'Karla', 'Prompt', 'Saira', 'Geologica', 'Bai Jamjuree', 'Niramit', 'Livvic', 'Exo', 'K2D', 'Jura', 'Philosopher', 'Montserrat', 'Open Sans', 'Rubik', 'Oswald','Work Sans', 'Mulish', 'Barlow', 'Heebo', 'Titillium Web', 'Libre Franklin', 'Josefin Sans', 'Jost', 'Outfit', 'Figtree', 'Overpass', 'Chivo', 'Alegreya Sans', 'Fahkwang'
        ]
      }
    ]
  }
}

const selectedFont = ref(
  JSON.parse(localStorage.getItem('currentState') || '{}')?.sceleton?.config?.theme?.fontFamily?.sans?.[0] || 'Nunito'
)
const selectedColor = ref(currentTheme.value || 'green')
const selectedRadius = ref(JSON.parse(localStorage.getItem('currentState') || '{}')?.sceleton?.radius || '0.5rem')

const { loadFont, updateFontLink } = useFont()

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

onMounted(() => {
  initializeTheme()
  if (currentTheme.value && currentTheme.value !== selectedColor.value) {
    selectedColor.value = currentTheme.value
    updateTheme()
  }
})
</script>

<template>
  <div class="relative">
    <button
      type="button"
      class="flex items-center justify-center rounded-full p-2 transition-colors hover:bg-accent hover:text-accent-foreground"
      @click="isOpen = !isOpen"
    >
      <Palette class="h-5 w-5" />
    </button>
    
    <div 
      v-if="isOpen"
      class="absolute right-0 top-10 z-50 w-80 rounded-lg border bg-background p-4 shadow-lg"
      @click.stop
    >
      <div class="space-y-4">
        <div>
          <h3 class="text-lg font-semibold">{{ sheetContent.header.title }}</h3>
          <p class="text-sm text-muted-foreground">{{ sheetContent.header.description }}</p>
        </div>
        
        <div class="space-y-4">
          <template v-for="section in sheetContent.theme.sections" :key="section.label">
            <div class="space-y-2">
              <label class="text-sm font-medium">{{ section.label }}</label>
              
              <div v-if="section.type === 'colors'" class="grid grid-cols-3 gap-2">
                <button 
                  v-for="color in section.options"
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

              <div v-else-if="section.type === 'radius'" class="grid grid-cols-5 gap-2">
                <button
                  v-for="radius in section.options"
                  :key="radius"
                  class="rounded-md border p-2 text-xs transition-colors hover:bg-accent"
                  :class="{ 'border-primary bg-accent': selectedRadius === radius }"
                  @click="selectedRadius = radius; updateTheme()"
                >
                  {{ formatRadius(radius) }}
                </button>
              </div>

              <select 
                v-else-if="section.type === 'font'"
                v-model="selectedFont"
                class="w-full rounded-md border bg-background px-3 py-2 text-sm"
                @change="updateTheme"
              >
                <option 
                  v-for="font in section.options"
                  :key="font"
                  :value="font"
                  :style="{ fontFamily: font }"
                >
                  {{ font }}
                </option>
              </select>
            </div>
          </template>
        </div>
      </div>
    </div>
    
    <div 
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="isOpen = false"
    />
  </div>
</template>