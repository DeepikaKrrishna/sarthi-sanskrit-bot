const BASE = '/api';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }
  return res.json();
}

export interface ChatApiRequest {
  message: string;
  conversation_history?: Array<{ role: 'user' | 'assistant'; content: string }>;
  learner_context?: { level: string; language: string };
}

export const api = {
  health: () => request<{ status: string; application: string; version: string }>('/health'),
  chat: (payload: ChatApiRequest) => request<any>('/chat', { method: 'POST', body: JSON.stringify(payload) }),
  translate: (text: string) => request<any>('/translate', { method: 'POST', body: JSON.stringify({ text }) }),
  meaning: (word: string) => request<any>('/meaning', { method: 'POST', body: JSON.stringify({ word }) }),
  grammarTopics: () => request<any[]>('/grammar/topics'),
  grammarTopic: (id: string) => request<any>(`/grammar/topics/${id}`),
  analyzeSentence: (sentence: string) => request<any>('/analyze-sentence', { method: 'POST', body: JSON.stringify({ sentence }) }),
  sandhiAll: () => request<any>('/sandhi'),
  sandhiAnalyze: (text: string) => request<any>('/sandhi', { method: 'POST', body: JSON.stringify({ text }) }),
  shlokas: () => request<any[]>('/shlokas'),
  shloka: (id: number) => request<any>(`/shlokas/${id}`),
  lessons: () => request<any[]>('/lessons'),
  lesson: (id: number) => request<any>(`/lessons/${id}`),
  quiz: (count?: number) => request<any[]>(`/quiz?count=${count || 10}`),
  dictionary: () => request<any[]>('/dictionary'),
};
