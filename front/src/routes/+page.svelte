<script lang="ts">
  import ChatContainer from '$lib/components/ChatContainer.svelte';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import { currentChatId, chats } from '$lib/stores/chat';

  const currentChat = $derived(
    $currentChatId ? $chats.find(c => c.id === $currentChatId) : null
  );
</script>

<div class="h-full flex flex-col bg-background">
  {#if currentChat}
    <ChatContainer chat={currentChat} />
  {:else}
    <EmptyState />
  {/if}
</div>