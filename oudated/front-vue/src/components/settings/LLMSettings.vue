<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium mb-4">Настройки LLM</h3>
      <p class="text-sm text-muted-foreground mb-4">
        Выберите провайдер языковой модели для генерации ответов
      </p>
    </div>

    <!-- Текущий статус -->
    <div class="bg-muted rounded-lg p-4">
      <div class="flex items-center gap-2 mb-2">
        <div :class="[
          'w-2 h-2 rounded-full',
          currentStatus?.status === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
        ]" />
        <span class="font-medium">
          {{ currentStatus?.status === 'ready' ? 'Активен' : 'Режим заглушки' }}
        </span>
      </div>
      <div class="text-sm text-muted-foreground">
        <div>Провайдер: {{ currentStatus?.provider || 'Не определен' }}</div>
        <div>Модель: {{ currentStatus?.model || 'Не определена' }}</div>
      </div>
    </div>

    <!-- Выбор провайдера -->
    <div class="space-y-4">
      <div>
        <label class="text-sm font-medium mb-2 block">Провайдер</label>
        <select 
          v-model="selectedProvider"
          @change="onProviderChange"
          class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option v-for="(provider, key) in providers" :key="key" :value="key">
            {{ provider.name }}
          </option>
        </select>
        <p v-if="selectedProviderInfo" class="text-xs text-muted-foreground mt-1">
          {{ selectedProviderInfo.description }}
        </p>
      </div>

      <!-- Выбор модели -->
      <div v-if="selectedProviderInfo">
        <label class="text-sm font-medium mb-2 block">Модель</label>
        <select 
          v-model="selectedModel"
          class="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option v-for="model in selectedProviderInfo.models" :key="model" :value="model">
            {{ model }}
          </option>
        </select>
      </div>

      <!-- API ключ -->
      <div v-if="selectedProviderInfo?.requires_api_key">
        <label class="text-sm font-medium mb-2 block">API Ключ</label>
        <div class="relative">
          <input
            v-model="apiKey"
            :type="showApiKey ? 'text' : 'password'"
            placeholder="Введите API ключ..."
            class="w-full rounded-lg border border-border bg-background px-3 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <button
            @click="showApiKey = !showApiKey"
            class="absolute right-2 top-2 p-1 hover:bg-muted rounded"
          >
            <Eye v-if="!showApiKey" class="w-4 h-4" />
            <EyeOff v-else class="w-4 h-4" />
          </button>
        </div>
        <p class="text-xs text-muted-foreground mt-1">
          {{ selectedProvider === 'openai' 
            ? 'Получите ключ на platform.openai.com' 
            : 'Получите ключ на console.anthropic.com' 
          }}
        </p>
      </div>

      <!-- Кнопка применить -->
      <button
        @click="applySettings"
        :disabled="isApplying || !canApply"
        class="w-full bg-primary text-primary-foreground rounded-lg px-4 py-2 text-sm font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <div v-if="isApplying" class="flex items-center justify-center gap-2">
          <Loader2 class="w-4 h-4 animate-spin" />
          Применяем...
        </div>
        <span v-else>Применить настройки</span>
      </button>

      <!-- Результат -->
      <div v-if="lastResult" :class="[
        'p-3 rounded-lg text-sm',
        lastResult.success 
          ? 'bg-green-100 text-green-800 border border-green-200' 
          : 'bg-red-100 text-red-800 border border-red-200'
      ]">
        {{ lastResult.message }}
      </div>
    </div>

    <!-- Информация о провайдерах -->
    <div class="space-y-3">
      <h4 class="font-medium">Доступные провайдеры:</h4>
      <div class="space-y-2">
        <div v-for="(provider, key) in providers" :key="key" 
             class="bg-muted rounded-lg p-3">
          <div class="flex items-center justify-between mb-1">
            <span class="font-medium">{{ provider.name }}</span>
            <span :class="[
              'text-xs px-2 py-1 rounded',
              provider.requires_api_key 
                ? 'bg-yellow-100 text-yellow-800' 
                : 'bg-green-100 text-green-800'
            ]">
              {{ provider.requires_api_key ? 'Нужен API ключ' : 'Бесплатно' }}
            </span>
          </div>
          <p class="text-xs text-muted-foreground">{{ provider.description }}</p>
          <div class="text-xs text-muted-foreground mt-1">
            Модели: {{ provider.models.join(', ') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Eye, EyeOff, Loader2 } from 'lucide-vue-next'
import { ragApi, type LLMProvider, type LLMConfig } from '@/api/ragApi'

// Реактивные данные
const providers = ref<Record<string, LLMProvider>>({})
const currentStatus = ref<any>(null)
const selectedProvider = ref('local')
const selectedModel = ref('')
const apiKey = ref('')
const showApiKey = ref(false)
const isApplying = ref(false)
const lastResult = ref<{ success: boolean; message: string } | null>(null)

// Вычисляемые свойства
const selectedProviderInfo = computed(() => {
  return providers.value[selectedProvider.value] || null
})

const canApply = computed(() => {
  if (!selectedProvider.value || !selectedModel.value) return false
  if (selectedProviderInfo.value?.requires_api_key && !apiKey.value.trim()) return false
  return true
})

// Методы
const loadProviders = async () => {
  try {
    const response = await ragApi.getLLMProviders()
    providers.value = response.providers
    
    // Устанавливаем первую модель по умолчанию
    if (providers.value[selectedProvider.value]) {
      selectedModel.value = providers.value[selectedProvider.value].models[0]
    }
  } catch (error) {
    console.error('Failed to load providers:', error)
  }
}

const loadCurrentStatus = async () => {
  try {
    currentStatus.value = await ragApi.getLLMStatus()
  } catch (error) {
    console.error('Failed to load LLM status:', error)
  }
}

const onProviderChange = () => {
  // Сбрасываем модель и API ключ при смене провайдера
  if (selectedProviderInfo.value) {
    selectedModel.value = selectedProviderInfo.value.models[0]
  }
  apiKey.value = ''
  lastResult.value = null
}

const applySettings = async () => {
  if (!canApply.value) return

  isApplying.value = true
  lastResult.value = null

  try {
    const config: LLMConfig = {
      provider: selectedProvider.value,
      model: selectedModel.value
    }

    if (selectedProviderInfo.value?.requires_api_key && apiKey.value.trim()) {
      config.api_key = apiKey.value.trim()
    }

    const result = await ragApi.configureLLM(config)
    
    lastResult.value = {
      success: true,
      message: result.message || 'Настройки успешно применены'
    }

    // Обновляем текущий статус
    await loadCurrentStatus()

  } catch (error) {
    lastResult.value = {
      success: false,
      message: error instanceof Error ? error.message : 'Ошибка применения настроек'
    }
  } finally {
    isApplying.value = false
  }
}

// Инициализация
onMounted(async () => {
  await Promise.all([
    loadProviders(),
    loadCurrentStatus()
  ])
})
</script>