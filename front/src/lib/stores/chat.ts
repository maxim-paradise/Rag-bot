import { writable } from "svelte/store";
import type { Message } from "$lib/types";

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  projectId?: string;
}

export interface Project {
  id: string;
  name: string;
  icon: string;
  color: string;
}

// Stores
export const chats = writable<Chat[]>([]);
export const currentChatId = writable<string | null>(null);
export const projects = writable<Project[]>([
  { id: "work", name: "Work", icon: "💼", color: "blue" },
  { id: "life", name: "Life", icon: "🌱", color: "green" },
  { id: "money", name: "Money", icon: "💰", color: "yellow" },
  { id: "ai", name: "Ai", icon: "🤖", color: "purple" },
]);
export const sidebarOpen = writable(true);

// Helper functions
export function createNewChat(projectId?: string): string {
  const newChat: Chat = {
    id: Date.now().toString(),
    title: "New chat",
    messages: [],
    createdAt: new Date(),
    updatedAt: new Date(),
    projectId,
  };

  chats.update((c) => [newChat, ...c]);
  currentChatId.set(newChat.id);

  return newChat.id;
}

export function updateChatTitle(chatId: string, title: string) {
  chats.update((c) =>
    c.map((chat) =>
      chat.id === chatId ? { ...chat, title, updatedAt: new Date() } : chat
    )
  );
}

export function addMessageToChat(chatId: string, message: Message) {
  chats.update((c) =>
    c.map((chat) => {
      if (chat.id === chatId) {
        const updatedMessages = [...chat.messages, message];
        // Auto-generate title from first user message
        const title =
          chat.messages.length === 0 && message.role === "user"
            ? message.content.slice(0, 50) +
              (message.content.length > 50 ? "..." : "")
            : chat.title;

        return {
          ...chat,
          messages: updatedMessages,
          title,
          updatedAt: new Date(),
        };
      }
      return chat;
    })
  );
}

export function deleteChat(chatId: string) {
  chats.update((c) => c.filter((chat) => chat.id !== chatId));
  currentChatId.update((id) => (id === chatId ? null : id));
}

export function getChatsByProject(projectId: string) {
  let allChats: Chat[] = [];
  chats.subscribe((c) => (allChats = c))();
  return allChats.filter((chat) => chat.projectId === projectId);
}
