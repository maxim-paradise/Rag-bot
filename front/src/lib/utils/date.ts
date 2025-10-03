export function formatDistanceToNow(date: Date): string {
  const now = new Date();
  const diffInMs = now.getTime() - date.getTime();
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));

  if (diffInMinutes < 1) return 'just now';
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
  if (diffInHours < 24) return `${diffInHours}h ago`;
  if (diffInDays < 7) return `${diffInDays}d ago`;
  
  return date.toLocaleDateString();
}

export function groupChatsByDate(chats: Array<{ updatedAt: Date }>) {
  const now = new Date();
  const today: typeof chats = [];
  const yesterday: typeof chats = [];
  const thisWeek: typeof chats = [];
  const older: typeof chats = [];

  chats.forEach(chat => {
    const daysDiff = Math.floor((now.getTime() - chat.updatedAt.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysDiff === 0) today.push(chat);
    else if (daysDiff === 1) yesterday.push(chat);
    else if (daysDiff <= 7) thisWeek.push(chat);
    else older.push(chat);
  });

  return { today, yesterday, thisWeek, older };
}
