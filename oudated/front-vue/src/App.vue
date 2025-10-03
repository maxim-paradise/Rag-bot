<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="h-screen bg-background flex flex-col">
    <div class="flex-1">
      <RouterView />
    </div>
  </div>
</template>