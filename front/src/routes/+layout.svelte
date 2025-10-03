<script lang="ts">
  import '../app.css';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import Header from '$lib/components/Header.svelte';
  
  let { children } = $props();
</script>

<svelte:head>
  <title>AI Chatbot RAG</title>
  <script>
    // Добавляем класс dark для темной темы
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  </script>
</svelte:head>

<div class="flex h-screen overflow-hidden bg-background">
  <Sidebar />
  
  <div class="flex-1 flex flex-col overflow-hidden">
    <Header />
    <main class="flex-1 overflow-hidden bg-background">
      {@render children?.()}
    </main>
  </div>
</div>
