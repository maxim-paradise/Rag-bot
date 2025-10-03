<script lang="ts">
  import { sidebarOpen } from '$lib/stores/chat';
  import ThemeToggle from './ThemeToggle.svelte';

  function toggleSidebar() {
    sidebarOpen.update(v => !v);
  }
</script>

<header class="h-14 border-b border-border bg-card flex items-center justify-between px-4">
  <div class="flex items-center gap-3">
    <button
      onclick={toggleSidebar}
      class="p-2 hover:bg-muted rounded-lg transition-colors"
      title="Toggle sidebar"
    >
      <svg class="w-5 h-5 text-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    
    <div class="flex items-center gap-2">
      <h2 class="text-lg font-semibold text-foreground">ChatGPT</h2>
      <button 
        class="p-1 hover:bg-muted rounded transition-colors"
        aria-label="Select model"
      >
        <svg class="w-4 h-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>
  </div>

  <div class="flex items-center gap-2">
    <ThemeToggle />
    
    <button 
      class="btn-primary px-4 py-2 text-sm font-medium rounded-lg flex items-center gap-2 shadow-lg"
      aria-label="Upgrade to ChatGPT Plus"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
      Get Plus
    </button>
  </div>
</header>
