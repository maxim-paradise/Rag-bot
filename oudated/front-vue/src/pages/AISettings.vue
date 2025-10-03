<template>
  <div class="min-h-screen bg-background">
    <!-- Header -->
    <div class="border-b bg-card">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <button 
              @click="goBack"
              class="p-2 hover:bg-accent rounded-md transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-2xl font-bold">AI Settings</h1>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto space-y-8">
        
        <!-- LLM Provider Configuration -->
        <div class="bg-card rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">LLM Provider</h2>
          
          <div class="space-y-4">
            <!-- Provider Selection -->
            <div>
              <label class="block text-sm font-medium mb-2">Provider</label>
              <select 
                v-model="selectedProvider"
                @change="loadProviderModels"
                class="w-full p-3 border rounded-lg bg-background"
              >
                <option value="">Select Provider</option>
                <option v-for="provider in providers" :key="provider.key" :value="provider.key">
                  {{ provider.name }}
                </option>
              </select>
            </div>

            <!-- Model Selection -->
            <div v-if="selectedProvider">
              <label class="block text-sm font-medium mb-2">Model</label>
              <select 
                v-model="selectedModel"
                class="w-full p-3 border rounded-lg bg-background"
              >
                <option value="">Select Model</option>
                <option v-for="model in availableModels" :key="model" :value="model">
                  {{ model }}
                </option>
              </select>
            </div>

            <!-- API Key Input -->
            <div v-if="requiresApiKey">
              <label class="block text-sm font-medium mb-2">API Key</label>
              <input 
                v-model="apiKey"
                type="password"
                placeholder="Enter your API key"
                class="w-full p-3 border rounded-lg bg-background"
              />
              <p class="text-sm text-muted-foreground mt-1">
                Your API key is stored locally and never shared
              </p>
            </div>

            <!-- Save Button -->
            <button 
              @click="saveConfiguration"
              :disabled="!canSave"
              class="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Save Configuration
            </button>
          </div>
        </div>

        <!-- Current Status -->
        <div class="bg-card rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">Current Status</h2>
          
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">Provider:</span>
              <span class="text-sm">{{ currentStatus.provider || 'Not configured' }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">Model:</span>
              <span class="text-sm">{{ currentStatus.model || 'Not configured' }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">Status:</span>
              <span 
                class="text-sm px-2 py-1 rounded"
                :class="currentStatus.status === 'ready' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
              >
                {{ currentStatus.status || 'Unknown' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Embeddings Configuration -->
        <div class="bg-card rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">Embeddings</h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Model</label>
              <select 
                v-model="embeddingsModel"
                class="w-full p-3 border rounded-lg bg-background"
              >
                <option value="cointegrated/rubert-tiny2">RuBERT Tiny2 (Russian)</option>
                <option value="all-MiniLM-L6-v2">All-MiniLM-L6-v2 (English)</option>
                <option value="paraphrase-multilingual-MiniLM-L12-v2">Multilingual MiniLM</option>
              </select>
            </div>
            
            <p class="text-sm text-muted-foreground">
              Embeddings model is used to create vector representations of text for semantic search.
            </p>
          </div>
        </div>

        <!-- System Information -->
        <div class="bg-card rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">System Information</h2>
          
          <div class="space-y-3" v-if="systemInfo">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">Documents in Database:</span>
              <span class="text-sm">{{ systemInfo.documents_count || 0 }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">Embeddings Model:</span>
              <span class="text-sm">{{ systemInfo.embeddings_model || 'Unknown' }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">System Status:</span>
              <span 
                class="text-sm px-2 py-1 rounded"
                :class="systemInfo.status === 'healthy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
              >
                {{ systemInfo.status || 'Unknown' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-card rounded-lg border p-6">
          <h2 class="text-xl font-semibold mb-4">Actions</h2>
          
          <div class="space-y-3">
            <button 
              @click="testConnection"
              :disabled="testing"
              class="w-full px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ testing ? 'Testing...' : 'Test Connection' }}
            </button>
            
            <button 
              @click="loadProviders"
              class="w-full px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              Refresh Providers
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ragApi } from '@/api/ragApi'

const router = useRouter()

// Reactive data
const selectedProvider = ref('')
const selectedModel = ref('')
const apiKey = ref('')
const embeddingsModel = ref('cointegrated/rubert-tiny2')
const testing = ref(false)

const providers = ref([
  {
    key: 'local',
    name: 'Local Model',
    models: ['microsoft/DialoGPT-medium', 'microsoft/DialoGPT-small', 'gpt2'],
    requiresApiKey: false,
    description: 'Works offline but slow'
  },
  {
    key: 'openai',
    name: 'OpenAI',
    models: ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo-preview'],
    requiresApiKey: true,
    description: 'Fast and high quality'
  },
  {
    key: 'anthropic',
    name: 'Anthropic Claude',
    models: ['claude-3-haiku-20240307', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229'],
    requiresApiKey: true,
    description: 'Very intelligent'
  }
])

const currentStatus = ref({
  provider: '',
  model: '',
  status: ''
})

const systemInfo = ref(null)

// Computed
const availableModels = computed(() => {
  const provider = providers.value.find(p => p.key === selectedProvider.value)
  return provider?.models || []
})

const requiresApiKey = computed(() => {
  const provider = providers.value.find(p => p.key === selectedProvider.value)
  return provider?.requiresApiKey || false
})

const canSave = computed(() => {
  if (!selectedProvider.value || !selectedModel.value) return false
  if (requiresApiKey.value && !apiKey.value.trim()) return false
  return true
})

// Methods
const goBack = () => {
  router.back()
}

const loadProviderModels = () => {
  selectedModel.value = ''
  if (availableModels.value.length > 0) {
    selectedModel.value = availableModels.value[0]
  }
}

const loadProviders = async () => {
  try {
    const response = await ragApi.getLLMProviders()
    if (response?.providers) {
      providers.value = Object.entries(response.providers).map(([key, value]: [string, any]) => ({
        key,
        ...value
      }))
    }
  } catch (error) {
    console.error('Failed to load providers:', error)
  }
}

const saveConfiguration = async () => {
  try {
    const config = {
      provider: selectedProvider.value,
      model: selectedModel.value,
      api_key: requiresApiKey.value ? apiKey.value : undefined
    }
    
    const response = await ragApi.configureLLM(config)
    if (response?.status === 'success') {
      // Reload status after successful configuration
      await loadCurrentStatus()
      alert('Configuration saved successfully!')
    }
  } catch (error) {
    console.error('Failed to save configuration:', error)
    alert('Failed to save configuration')
  }
}

const loadCurrentStatus = async () => {
  try {
    const response = await ragApi.getLLMStatus()
    currentStatus.value = response || {}
  } catch (error) {
    console.error('Failed to load current status:', error)
  }
}

const loadSystemInfo = async () => {
  try {
    const response = await ragApi.healthCheck()
    systemInfo.value = response || {}
  } catch (error) {
    console.error('Failed to load system info:', error)
  }
}

const testConnection = async () => {
  testing.value = true
  try {
    await loadCurrentStatus()
    await loadSystemInfo()
    alert('Connection test completed!')
  } catch (error) {
    console.error('Connection test failed:', error)
    alert('Connection test failed')
  } finally {
    testing.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadProviders(),
    loadCurrentStatus(),
    loadSystemInfo()
  ])
})
</script>

<style scoped>
/* Add any custom styles here */
</style>