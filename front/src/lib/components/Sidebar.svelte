<script lang="ts">
  import { sidebarOpen, currentChatId, createNewChat, projects, chats } from '$lib/stores/chat';
  import ChatList from './ChatList.svelte';
  import ProjectList from './ProjectList.svelte';
  import { slide } from 'svelte/transition';

  let showGPTs = $state(false);
  let selectedProject = $state<string | null>(null);

  function handleNewChat() {
    createNewChat(selectedProject || undefined);
  }

  function toggleGPTs() {
    showGPTs = !showGPTs;
  }

  function selectProject(projectId: string | null) {
    selectedProject = projectId;
  }
</script>

{#if $sidebarOpen}
  <aside 
    class="sidebar w-64 flex flex-col h-screen border-r"
    transition:slide={{ axis: 'x', duration: 200 }}
  >
    <!-- Header -->
    <div class="p-3 border-b">
      <button
        onclick={handleNewChat}
        class="sidebar-item w-full flex items-center gap-2 px-3 py-2.5 rounded-lg"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span class="font-medium">New chat</span>
      </button>
    </div>

    <!-- Search -->
    <div class="p-3 border-b">
      <button class="sidebar-item w-full flex items-center gap-2 px-3 py-2 rounded-lg opacity-70">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <span class="text-sm">Search chats</span>
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- GPTs Section -->
      <div class="p-2 border-b">
        <h3 class="px-3 py-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          GPTs
        </h3>
        <button class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg">
          <div class="w-6 h-6 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xs">
            ✨
          </div>
          <span class="text-sm font-medium">Explore</span>
        </button>
        <button class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg">
          <div class="avatar-ai w-6 h-6 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <span class="text-sm font-medium">Code Copilot</span>
        </button>
        <button class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg">
          <div class="w-6 h-6 rounded-full bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="text-sm font-medium">Wolfram</span>
        </button>
        <button class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg">
          <div class="w-6 h-6 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center text-xs">
            🛒
          </div>
          <span class="text-sm font-medium">Shopping Assistant</span>
        </button>
      </div>

      <!-- Projects -->
      <ProjectList onSelectProject={selectProject} {selectedProject} />

      <!-- Chats -->
      <div class="p-2">
        <h3 class="px-3 py-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          Chats
        </h3>
        <ChatList projectFilter={selectedProject} />
      </div>
    </div>

    <!-- User Profile -->
    <div class="p-3 border-t">
      <div class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg">
        <div class="avatar-ai w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold text-white">
          M
        </div>
        <div class="flex-1 text-left">
          <div class="text-sm font-medium">Максим Райс...</div>
          <div class="text-xs text-muted-foreground">Free</div>
        </div>
        <button 
          class="px-2 py-1 text-xs font-semibold bg-muted hover:bg-accent rounded transition-colors"
          aria-label="Upgrade to Plus"
        >
          Upgrade
        </button>
      </div>
    </div>
  </aside>
{/if}
