<script lang="ts">
	interface Props {
		isLoading: boolean;
		onSend: (message: string) => void;
	}

	let { isLoading, onSend }: Props = $props();
	let inputValue = $state('');
	let textarea: HTMLTextAreaElement;

	function handleSubmit() {
		const message = inputValue.trim();
		if (message && !isLoading) {
			onSend(message);
			inputValue = '';
			if (textarea) {
				textarea.style.height = 'auto';
			}
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSubmit();
		}
	}

	function autoResize() {
		if (textarea) {
			textarea.style.height = 'auto';
			textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
		}
	}
</script>

<div class="p-4 bg-background">
  <form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="flex gap-3 items-end">
    <div class="flex-1 relative">
      <textarea
        bind:this={textarea}
        bind:value={inputValue}
        oninput={autoResize}
        onkeydown={handleKeydown}
        placeholder="Ask anything..."
        disabled={isLoading}
        rows="1"
        class="input-field w-full px-4 py-3 pr-12 resize-none transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
      ></textarea>
    </div>
    
    <button
      type="submit"
      disabled={!inputValue.trim() || isLoading}
      class="flex-shrink-0 w-10 h-10 rounded-xl bg-muted hover:bg-accent text-foreground flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
    >
      {#if isLoading}
        <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      {:else}
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      {/if}
    </button>
  </form>
</div>