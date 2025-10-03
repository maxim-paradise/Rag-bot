<template>
  <nav class="bg-card border-b border-border">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <!-- Логотип -->
          <div class="flex items-center gap-2">
            <Bot class="w-6 h-6 text-primary" />
            <h1 class="text-xl font-bold text-foreground">
              AI Система
            </h1>
          </div>
        </div>

        <div class="flex items-center">
          <span class="text-sm text-muted-foreground">
            Единая платформа для работы с AI
          </span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Bot } from 'lucide-vue-next'
</script>