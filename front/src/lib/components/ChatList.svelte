<script lang="ts">
  import { chats, currentChatId, deleteChat } from '$lib/stores/chat';
  import { formatDistanceToNow } from '$lib/utils/date';

  interface Props {
    projectFilter?: string | null;
  }

  let { projectFilter = null }: Props = $props();

  let hoveredChatId = $state<string | null>(null);

  const filteredChats = $derived(
    projectFilter 
      ? $chats.filter(chat => chat.projectId === projectFilter)
      : $chats
  );

  const groupedChats = $derived(() => {
    const now = new Date();
    const today: typeof filteredChats = [];
    const yesterday: typeof filteredChats = [];
    const thisWeek: typeof filteredChats = [];
    const older: typeof filteredChats = [];

    filteredChats.forEach(chat => {
      const daysDiff = Math.floor((now.getTime() - chat.updatedAt.getTime()) / (1000 * 60 * 60 * 24));
      
      if (daysDiff === 0) today.push(chat);
      else if (daysDiff === 1) yesterday.push(chat);
      else if (daysDiff <= 7) thisWeek.push(chat);
      else older.push(chat);
    });

    return { today, yesterday, thisWeek, older };
  });

  function selectChat(chatId: string) {
    currentChatId.set(chatId);
  }

  function handleDeleteChat(chatId: string, event: Event) {
    event.stopPropagation();
    if (confirm('Delete this chat?')) {
      deleteChat(chatId);
    }
  }
</script>

<div class="space-y-4">
  {#each Object.entries(groupedChats()) as [period, periodChats]}
    {#if periodChats.length > 0}
      <div>
        <h4 class="px-3 py-1 text-xs font-medium text-muted-foreground capitalize">
          {period === 'today' ? 'Today' : period === 'yesterday' ? 'Yesterday' : period === 'thisWeek' ? 'This Week' : 'Older'}
        </h4>
        <div class="space-y-0.5">
          {#each periodChats as chat (chat.id)}
            <div
              role="button"
              tabindex="0"
              onclick={() => selectChat(chat.id)}
              onmouseenter={() => hoveredChatId = chat.id}
              onmouseleave={() => hoveredChatId = null}
              onkeydown={(e) => e.key === 'Enter' && selectChat(chat.id)}
              class="sidebar-item w-full flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer {$currentChatId === chat.id ? 'active' : ''}"
            >
              <svg class="w-4 h-4 text-muted-foreground flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <span class="text-sm truncate flex-1 text-left">
                {chat.title}
              </span>
              {#if hoveredChatId === chat.id}
                <button
                  onclick={(e) => handleDeleteChat(chat.id, e)}
                  class="opacity-0 group-hover:opacity-100 p-1 hover:bg-destructive/10 rounded transition-all"
                  aria-label="Delete chat"
                >
                  <svg class="w-4 h-4 text-muted-foreground hover:text-destructive" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}
  {/each}

  {#if filteredChats.length === 0}
    <div class="px-3 py-8 text-center text-muted-foreground text-sm">
      No chats yet. Start a new conversation!
    </div>
  {/if}
</div>
