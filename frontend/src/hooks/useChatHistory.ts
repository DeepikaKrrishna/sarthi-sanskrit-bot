import { useState, useCallback } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  act?: any;
  timestamp: number;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: number;
  updatedAt: number;
}

const STORAGE_KEY = 'sarthi_conversations';

function load(): Conversation[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

function save(convos: Conversation[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convos));
}

function makeId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

export function useChatHistory() {
  const [conversations, setConversations] = useState<Conversation[]>(load);
  const [activeId, setActiveId] = useState<string | null>(
    () => load()[0]?.id ?? null
  );

  const active = conversations.find(c => c.id === activeId) ?? null;

  const persist = useCallback((next: Conversation[]) => {
    setConversations(next);
    save(next);
  }, []);

  const newChat = useCallback(() => {
    const c: Conversation = {
      id: makeId(),
      title: 'New conversation',
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    const next = [c, ...conversations];
    persist(next);
    setActiveId(c.id);
    return c.id;
  }, [conversations, persist]);

  const addMessage = useCallback((convId: string, msg: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    setConversations(prev => {
      const next = prev.map(c => {
        if (c.id !== convId) return c;
        const newMsg: ChatMessage = { ...msg, id: makeId(), timestamp: Date.now() };
        const messages = [...c.messages, newMsg];
        const title = c.messages.length === 0 && msg.role === 'user'
          ? msg.content.replace(/[.!?]+$/, '').slice(0, 48).trim() || 'Untitled conversation'
          : c.title;
        return { ...c, messages, title, updatedAt: Date.now() };
      });
      save(next);
      return next;
    });
  }, []);

  const deleteConversation = useCallback((id: string) => {
    const next = conversations.filter(c => c.id !== id);
    persist(next);
    if (activeId === id) setActiveId(next[0]?.id ?? null);
  }, [conversations, activeId, persist]);

  const clearAll = useCallback(() => {
    persist([]);
    setActiveId(null);
  }, [persist]);

  return { conversations, active, activeId, setActiveId, newChat, addMessage, deleteConversation, clearAll };
}
