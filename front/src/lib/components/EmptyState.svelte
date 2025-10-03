<script lang="ts">
  import { createNewChat } from '$lib/stores/chat';

  const suggestions = [
    {
      icon: '💡',
      title: 'Create image',
      description: 'Generate and edit images with DALL·E'
    },
    {
      icon: '📊',
      title: 'Analyze data',
      description: 'Upload a file and ask questions about it'
    },
    {
      icon: '✍️',
      title: 'Write content',
      description: 'Create articles, stories, or any text'
    },
    {
      icon: '🔍',
      title: 'Get advice',
      description: 'Ask for recommendations and guidance'
    }
  ];

  function handleSuggestionClick() {
    createNewChat();
  }
</script>

<div class="h-full flex flex-col items-center justify-center p-8">
  <div class="max-w-3xl w-full space-y-8 animate-fade-in">
    <!-- Welcome Message -->
    <div class="text-center space-y-4">
      <div class="avatar-ai inline-flex items-center justify-center w-16 h-16 rounded-full mb-4">
        <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      </div>
      <h1 class="text-4xl font-bold text-foreground">
        Hey, Maxim. Ready to dive in?
      </h1>
      <p class="text-lg text-muted-foreground">
        Start a conversation or choose from the suggestions below
      </p>
    </div>

    <!-- Suggestions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#each suggestions as suggestion}
        <button
          onclick={handleSuggestionClick}
          class="group p-6 bg-card hover:bg-muted rounded-2xl transition-all border border-border hover:border-primary/50 hover:shadow-lg text-left"
        >
          <div class="flex items-start gap-4">
            <div class="text-3xl">{suggestion.icon}</div>
            <div class="flex-1">
              <h3 class="font-semibold text-foreground mb-1 group-hover:text-primary transition-colors">
                {suggestion.title}
              </h3>
              <p class="text-sm text-muted-foreground">
                {suggestion.description}
              </p>
            </div>
            <svg class="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors opacity-0 group-hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>
        </button>
      {/each}
    </div>

    <!-- Quick Actions -->
    <div class="flex flex-wrap gap-3 justify-center pt-8">
      <button class="px-4 py-2 bg-card border border-border rounded-lg hover:border-primary/30 hover:bg-muted transition-colors text-sm font-medium text-foreground">
        📄 Upload file
      </button>
      <button class="px-4 py-2 bg-card border border-border rounded-lg hover:border-primary/30 hover:bg-muted transition-colors text-sm font-medium text-foreground">
        🎨 Generate image
      </button>
      <button class="px-4 py-2 bg-card border border-border rounded-lg hover:border-primary/30 hover:bg-muted transition-colors text-sm font-medium text-foreground">
        💻 Write code
      </button>
    </div>
  </div>
</div>
