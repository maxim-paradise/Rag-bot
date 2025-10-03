<script lang="ts">
  import { projects, type Project } from '$lib/stores/chat';

  interface Props {
    onSelectProject: (projectId: string | null) => void;
    selectedProject: string | null;
  }

  let { onSelectProject, selectedProject }: Props = $props();

  function handleProjectClick(projectId: string) {
    onSelectProject(selectedProject === projectId ? null : projectId);
  }

  const colorClasses: Record<string, string> = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    yellow: 'from-yellow-500 to-yellow-600',
    purple: 'from-purple-500 to-purple-600',
  };
</script>

<div class="p-2 border-b">
  <h3 class="px-3 py-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
    Projects
  </h3>
  <div class="space-y-0.5">
    {#each $projects as project (project.id)}
      <button
        onclick={() => handleProjectClick(project.id)}
        class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg {selectedProject === project.id ? 'active' : ''}"
      >
        <div class="w-6 h-6 rounded-full bg-gradient-to-br {colorClasses[project.color]} flex items-center justify-center text-xs">
          {project.icon}
        </div>
        <span class="text-sm font-medium">{project.name}</span>
        {#if selectedProject === project.id}
          <svg class="w-4 h-4 ml-auto text-primary" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        {/if}
      </button>
    {/each}
    <button class="sidebar-item w-full flex items-center gap-3 px-3 py-2 rounded-lg opacity-60">
      <div class="w-6 h-6 rounded-full border-2 border-dashed border-current flex items-center justify-center">
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </div>
      <span class="text-sm">New project</span>
    </button>
  </div>
</div>
