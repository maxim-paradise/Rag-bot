<script lang="ts">
  import ChatMessage from './ChatMessage.svelte';
  import ChatInput from './ChatInput.svelte';
  import { addMessageToChat, type Chat } from '$lib/stores/chat';
  import type { Message } from '$lib/types';

  interface Props {
    chat: Chat;
  }

  let { chat }: Props = $props();
  let isLoading = $state(false);
  let chatContainer: HTMLDivElement;

  async function sendMessage(content: string) {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date()
    };

    addMessageToChat(chat.id, userMessage);
    isLoading = true;

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: content })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.message || 'Извините, произошла ошибка.',
        role: 'assistant',
        timestamp: new Date(),
        sources: data.sources
      };

      addMessageToChat(chat.id, assistantMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Извините, не удалось получить ответ. Пожалуйста, попробуйте позже.',
        role: 'assistant',
        timestamp: new Date()
      };

      addMessageToChat(chat.id, errorMessage);
    } finally {
      isLoading = false;
    }
  }

  function scrollToBottom() {
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }

  $effect(() => {
    if (chat.messages.length) {
      scrollToBottom();
    }
  });
</script>

<div class="h-full flex flex-col">
  <!-- Chat Messages -->
  <div
    bind:this={chatContainer}
    class="flex-1 overflow-y-auto p-6 space-y-4 scroll-smooth max-w-4xl mx-auto w-full"
  >
    {#each chat.messages as message (message.id)}
      <ChatMessage {message} />
    {/each}
    
    {#if isLoading}
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div class="flex-1 bg-slate-100 dark:bg-slate-700 rounded-2xl rounded-tl-none p-4">
          <div class="flex gap-1">
            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Chat Input -->
  <div class="border-t border-slate-200 dark:border-slate-700 max-w-4xl mx-auto w-full">
    <ChatInput {isLoading} onSend={sendMessage} />
  </div>
</div>