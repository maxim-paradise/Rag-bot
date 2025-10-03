<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
    @click.self="$emit('close')"
  >
    <div class="bg-card rounded-lg shadow-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
      <!-- Заголовок -->
      <div class="flex items-center justify-between p-6 border-b border-border">
        <div class="flex items-center gap-3">
          <Bot class="w-6 h-6 text-primary" />
          <h2 class="text-xl font-semibold">AI Настройки</h2>
        </div>
        <button
          @click="$emit('close')"
          class="p-2 hover:bg-muted rounded-lg transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Вкладки -->
      <div class="border-b border-border">
        <div class="flex">
          <button
            @click="activeTab = 'chat'"
            :class="[
              'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'chat'
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            ]"
          >
            <div class="flex items-center gap-2">
              <MessageSquare class="w-4 h-4" />
              Простой чат
            </div>
          </button>
          <button
            @click="activeTab = 'rag'"
            :class="[
              'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'rag'
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            ]"
          >
            <div class="flex items-center gap-2">
              <FileText class="w-4 h-4" />
              RAG Система
            </div>
          </button>
          <button
            @click="activeTab = 'llm'"
            :class="[
              'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
              activeTab === 'llm'
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            ]"
          >
            <div class="flex items-center gap-2">
              <Settings class="w-4 h-4" />
              LLM Настройки
            </div>
          </button>
        </div>
      </div>

      <!-- Содержимое -->
      <div class="p-6 overflow-y-auto max-h-[70vh]">
        <!-- Простой чат -->
        <div v-if="activeTab === 'chat'" class="space-y-6">
          <div>
            <h3 class="text-lg font-medium mb-4">Простой AI Чат</h3>
            <p class="text-muted-foreground mb-4">
              Общайтесь с искусственным интеллектом без загрузки документов
            </p>
          </div>

          <!-- Статус LLM -->
          <div class="bg-muted rounded-lg p-4">
            <div class="flex items-center gap-2 mb-2">
              <div :class="[
                'w-2 h-2 rounded-full',
                llmStatus?.status === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
              ]" />
              <span class="font-medium">
                {{ llmStatus?.status === 'ready' ? 'LLM готов' : 'Режим заглушки' }}
              </span>
            </div>
            <div class="text-sm text-muted-foreground">
              <div>Провайдер: {{ llmStatus?.provider || 'Не определен' }}</div>
              <div>Модель: {{ llmStatus?.model || 'Не определена' }}</div>
            </div>
          </div>

          <!-- Быстрые действия -->
          <div class="space-y-3">
            <h4 class="font-medium">Быстрые действия:</h4>
            <div class="grid grid-cols-2 gap-3">
              <button
                @click="testSimpleChat"
                :disabled="isTestingChat"
                class="p-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
              >
                <div v-if="isTestingChat" class="flex items-center justify-center gap-2">
                  <Loader2 class="w-4 h-4 animate-spin" />
                  Тестируем...
                </div>
                <span v-else>Тест чата</span>
              </button>
              <button
                @click="activeTab = 'llm'"
                class="p-3 bg-muted hover:bg-muted/80 rounded-lg transition-colors"
              >
                Настроить LLM
              </button>
            </div>
          </div>
        </div>

        <!-- RAG Система -->
        <div v-if="activeTab === 'rag'" class="space-y-6">
          <div>
            <h3 class="text-lg font-medium mb-4">RAG Система</h3>
            <p class="text-muted-foreground mb-4">
              Загружайте документы и задавайте вопросы по их содержанию
            </p>
          </div>

          <!-- Статус системы -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-muted rounded-lg p-4">
              <div class="flex items-center gap-2 mb-2">
                <div :class="[
                  'w-2 h-2 rounded-full',
                  llmStatus?.status === 'ready' ? 'bg-green-500' : 'bg-yellow-500'
                ]" />
                <span class="font-medium">LLM</span>
              </div>
              <div class="text-sm text-muted-foreground">
                {{ llmStatus?.provider || 'Не настроен' }}
              </div>
            </div>
            <div class="bg-muted rounded-lg p-4">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-2 h-2 rounded-full bg-blue-500" />
                <span class="font-medium">Документы</span>
              </div>
              <div class="text-sm text-muted-foreground">
                {{ documentsCount }} загружено
              </div>
            </div>
          </div>

          <!-- Управление документами -->
          <div class="space-y-4">
            <h4 class="font-medium">Управление документами:</h4>
            <DocumentManager 
              @documents-updated="onDocumentsUpdated"
              @document-uploaded="onDocumentUploaded"
            />
          </div>
        </div>

        <!-- LLM Настройки -->
        <div v-if="activeTab === 'llm'">
          <LLMSettings @settings-applied="onLLMSettingsApplied" />
        </div>
      </div>

      <!-- Результат тестирования -->
      <div v-if="testResult" class="p-4 border-t border-border">
        <div :class="[
          'p-3 rounded-lg text-sm',
          testResult.success 
            ? 'bg-green-100 text-green-800 border border-green-200' 
            : 'bg-red-100 text-red-800 border border-red-200'
        ]">
          <div class="font-medium mb-1">
            {{ testResult.success ? 'Тест прошел успешно!' : 'Ошибка теста' }}
          </div>
          <div>{{ testResult.message }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  Bot, X, MessageSquare, FileText, Settings, Loader2 
} from 'lucide-vue-next'
import { ragApi } from '@/api/ragApi'
import LLMSettings from './LLMSettings.vue'
import DocumentManager from '@/components/documents/DocumentManager.vue'

// Props
defineProps<{
  isOpen: boolean
}>()

// Emits
defineEmits<{
  close: []
}>()

// Реактивные данные
const activeTab = ref<'chat' | 'rag' | 'llm'>('chat')
const llmStatus = ref<any>(null)
const documentsCount = ref(0)
const isTestingChat = ref(false)
const testResult = ref<{ success: boolean; message: string } | null>(null)

// Методы
const loadSystemStatus = async () => {
  try {
    const [llmStatusResponse, documentsResponse] = await Promise.all([
      ragApi.getLLMStatus(),
      ragApi.getDocuments()
    ])
    
    llmStatus.value = llmStatusResponse
    documentsCount.value = documentsResponse.total_documents
  } catch (error) {
    console.error('Failed to load system status:', error)
  }
}

const testSimpleChat = async () => {
  isTestingChat.value = true
  testResult.value = null

  try {
    const response = await ragApi.simpleChat('Привет! Это тест AI системы.')
    
    testResult.value = {
      success: true,
      message: `AI ответил: "${response.response.slice(0, 100)}${response.response.length > 100 ? '...' : ''}"`
    }
  } catch (error) {
    testResult.value = {
      success: false,
      message: error instanceof Error ? error.message : 'Неизвестная ошибка'
    }
  } finally {
    isTestingChat.value = false
  }
}

const onLLMSettingsApplied = async () => {
  await loadSystemStatus()
  testResult.value = null
}

const onDocumentsUpdated = async () => {
  await loadSystemStatus()
}

const onDocumentUploaded = async () => {
  await loadSystemStatus()
}

// Инициализация
onMounted(async () => {
  await loadSystemStatus()
})
</script>