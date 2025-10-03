<script lang="ts">
	import type { Message } from '$lib/types';

	interface Props {
		message: Message;
	}

	let { message }: Props = $props();
	
	const isUser = message.role === 'user';
</script>

<div class="flex items-start gap-3 {isUser ? 'flex-row-reverse' : ''}">
  <!-- Avatar -->
  <div class="flex-shrink-0 w-8 h-8 rounded-full {isUser ? 'avatar-user' : 'avatar-ai'} flex items-center justify-center">
    {#if isUser}
      <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    {:else}
      <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    {/if}
  </div>

  <!-- Message Content -->
  <div class="flex-1 max-w-[80%]">
    <div class="{isUser ? 'message-user text-white' : 'message-ai text-foreground'} rounded-2xl {isUser ? 'rounded-tr-none' : 'rounded-tl-none'} p-4 shadow-md">
      <p class="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
    </div>
    
    <!-- Sources if available -->
    {#if message.sources && message.sources.length > 0}
      <div class="mt-2 px-2">
        <p class="text-xs text-muted-foreground mb-1">Источники:</p>
        <div class="space-y-1">
          {#each message.sources as source}
            <div class="text-xs bg-muted text-foreground rounded px-2 py-1">
              📄 {source}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Timestamp -->
    <p class="text-xs text-muted-foreground mt-1 {isUser ? 'text-right' : 'text-left'} px-2">
      {message.timestamp.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
    </p>
  </div>
</div>