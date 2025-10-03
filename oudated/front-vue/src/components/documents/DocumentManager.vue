<template>
  <div class="space-y-4">
    <!-- Загрузка документов -->
    <div>
      <h4 class="font-medium mb-3">Загрузить документы</h4>
      
      <div
        @drop="handleDrop"
        @dragover.prevent
        @dragenter.prevent
        :class="[
          'border-2 border-dashed rounded-lg p-4 text-center transition-colors cursor-pointer',
          isDragOver ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'
        ]"
        @click="triggerFileInput"
        @dragenter="isDragOver = true"
        @dragleave="isDragOver = false"
      >
        <input
          ref="fileInput"
          type="file"
          multiple
          accept=".txt,.md,.pdf,.docx,.doc,.py,.js,.html,.css"
          @change="handleFileSelect"
          class="hidden"
        />
        
        <Upload class="w-6 h-6 mx-auto mb-2 text-muted-foreground" />
        <p class="text-xs text-muted-foreground">
          Перетащите файлы или нажмите
        </p>
        <p class="text-xs text-muted-foreground mt-1">
          TXT, MD, PDF, DOCX, PY, JS, HTML, CSS
        </p>
      </div>

      <!-- Прогресс загрузки -->
      <div v-if="uploadProgress.length > 0" class="mt-3 space-y-2">
        <div v-for="progress in uploadProgress" :key="progress.filename" 
             class="text-xs bg-muted rounded p-2">
          <div class="flex justify-between items-center">
            <span class="truncate">{{ progress.filename }}</span>
            <span :class="[
              progress.status === 'success' ? 'text-green-600' : 
              progress.status === 'error' ? 'text-red-600' : 'text-blue-600'
            ]">
              {{ progress.status === 'uploading' ? 'Загрузка...' : 
                 progress.status === 'success' ? 'Готово' : 'Ошибка' }}
            </span>
          </div>
          <div v-if="progress.error" class="text-red-600 mt-1">
            {{ progress.error }}
          </div>
        </div>
      </div>
    </div>

    <!-- Список документов -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h4 class="font-medium">Документы ({{ documents.length }})</h4>
        <button
          v-if="documents.length > 0"
          @click="refreshDocuments"
          :disabled="documentsLoading"
          class="p-1 hover:bg-muted rounded transition-colors"
          title="Обновить список"
        >
          <RotateCcw :class="['w-4 h-4', documentsLoading && 'animate-spin']" />
        </button>
      </div>
      
      <div class="space-y-2 max-h-60 overflow-y-auto">
        <div v-if="documentsLoading" class="text-center py-4">
          <Loader2 class="w-4 h-4 animate-spin mx-auto mb-2" />
          <p class="text-xs text-muted-foreground">Загрузка документов...</p>
        </div>
        
        <div v-else-if="documents.length === 0" class="text-center py-4">
          <FileText class="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
          <p class="text-xs text-muted-foreground">Нет загруженных документов</p>
        </div>
        
        <div v-else>
          <div v-for="doc in documents" :key="doc.id" 
               class="bg-muted rounded-lg p-3 hover:bg-muted/80 transition-colors group">
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <h5 class="font-medium text-sm truncate">{{ doc.filename }}</h5>
                <p class="text-xs text-muted-foreground mt-1">
                  {{ formatFileSize(doc.content_length) }} • {{ doc.file_extension }}
                </p>
                <p v-if="doc.content_preview" class="text-xs text-muted-foreground mt-1 line-clamp-2">
                  {{ doc.content_preview }}
                </p>
              </div>
              <button
                @click="deleteDocument(doc.id)"
                class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-destructive/10 rounded"
                :disabled="deletingDocuments.has(doc.id)"
                title="Удалить документ"
              >
                <Trash2 class="w-4 h-4 text-destructive" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Действия -->
    <div v-if="documents.length > 0" class="pt-2 border-t border-border">
      <button
        @click="clearAllDocuments"
        :disabled="deletingDocuments.size > 0"
        class="w-full text-xs text-destructive hover:bg-destructive/10 py-2 rounded-lg transition-colors"
      >
        Очистить все документы
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Upload, FileText, Trash2, Loader2, RotateCcw } from 'lucide-vue-next'
import { ragApi, type Document } from '@/api/ragApi'

// Эмиты
const emit = defineEmits<{
  documentsUpdated: []
  documentUploaded: []
}>()

// Реактивные данные
const documents = ref<Document[]>([])
const documentsLoading = ref(false)
const deletingDocuments = ref(new Set<string>())
const isDragOver = ref(false)

const uploadProgress = ref<Array<{
  filename: string
  status: 'uploading' | 'success' | 'error'
  error?: string
}>>([])

// Refs
const fileInput = ref<HTMLInputElement>()

// Методы
const loadDocuments = async () => {
  documentsLoading.value = true
  try {
    const response = await ragApi.getDocuments()
    documents.value = response.documents
    emit('documentsUpdated')
  } catch (error) {
    console.error('Failed to load documents:', error)
  } finally {
    documentsLoading.value = false
  }
}

const refreshDocuments = async () => {
  await loadDocuments()
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    uploadFiles(Array.from(target.files))
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  
  if (event.dataTransfer?.files) {
    uploadFiles(Array.from(event.dataTransfer.files))
  }
}

const uploadFiles = async (files: File[]) => {
  // Инициализируем прогресс
  uploadProgress.value = files.map(file => ({
    filename: file.name,
    status: 'uploading' as const
  }))

  try {
    const result = await ragApi.uploadDocuments(files)
    
    // Обновляем прогресс на основе результатов
    uploadProgress.value = result.results.map(r => ({
      filename: r.filename,
      status: r.status,
      error: r.error
    }))

    // Перезагружаем список документов
    await loadDocuments()
    emit('documentUploaded')

    // Очищаем прогресс через 3 секунды
    setTimeout(() => {
      uploadProgress.value = []
    }, 3000)

  } catch (error) {
    console.error('Upload failed:', error)
    uploadProgress.value = uploadProgress.value.map(p => ({
      ...p,
      status: 'error' as const,
      error: 'Ошибка загрузки'
    }))
  }
}

const deleteDocument = async (docId: string) => {
  deletingDocuments.value.add(docId)
  try {
    await ragApi.deleteDocument(docId)
    await loadDocuments()
  } catch (error) {
    console.error('Delete failed:', error)
  } finally {
    deletingDocuments.value.delete(docId)
  }
}

const clearAllDocuments = async () => {
  if (!confirm('Вы уверены, что хотите удалить все документы?')) return
  
  const docIds = documents.value.map(doc => doc.id)
  
  for (const docId of docIds) {
    deletingDocuments.value.add(docId)
    try {
      await ragApi.deleteDocument(docId)
    } catch (error) {
      console.error('Delete failed:', error)
    } finally {
      deletingDocuments.value.delete(docId)
    }
  }
  
  await loadDocuments()
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Инициализация
onMounted(async () => {
  await loadDocuments()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>