import { useEffect, useRef, useState } from 'react';
import { Bot, Check, ChevronRight, Copy, Headphones, Loader2, Mic, MicOff, Send, Sparkles, Volume2 } from 'lucide-react';
import { api } from '../services/api';
import { Markdown } from '../components/Markdown';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  source?: string;
  aiUnavailable?: boolean;
  act?: any;
}

const STARTERS = [
  'Explain Sanskrit grammar to me',
  'Translate this sentence',
  'What does नमस्ते mean?',
  'Teach me Sandhi',
  'Give me a Sanskrit quiz',
  'Explain this shloka',
];

export function ChatPage({ chat }: { chat: any }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [thinking, setThinking] = useState('Understanding your question...');
  const [lastIntent, setLastIntent] = useState('');
  const [copied, setCopied] = useState<string | null>(null);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);
  const messages: Message[] = (chat.active?.messages ?? []) as Message[];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length, loading]);

  const getHistory = () => messages
    .filter((message: Message) => message.role === 'user' || message.role === 'assistant')
    .slice(-12)
    .map((message: Message) => ({ role: message.role, content: message.content }));

  const sendMessage = async (text = input) => {
    const cleanText = text.trim();
    if (!cleanText || loading) return;
    setInput('');
    setError('');
    const convId = chat.activeId ?? chat.newChat();
    chat.addMessage(convId, { role: 'user', content: cleanText });
    setLoading(true);
    setThinking('Analyzing your request...');

    try {
      const result = await api.chat({
        message: cleanText,
        conversation_history: getHistory().slice(0, -1),
        learner_context: { level: 'beginner', language: 'en' },
      });
      setLastIntent(result.intent || '');
      setThinking('Preparing a helpful response...');
      chat.addMessage(convId, {
        role: 'assistant',
        content: result.response,
        intent: result.intent,
        source: result.source,
        aiUnavailable: result.ai_unavailable,
        act: result.act,
      });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'SĀRTHI could not process that request.');
      chat.addMessage(convId, {
        role: 'assistant',
        content: 'SĀRTHI is temporarily unavailable. Please try again or use the local Sanskrit tools from the navigation.',
      });
    } finally {
      setLoading(false);
      setThinking('');
    }
  };

  const copyMessage = async (message: Message) => {
    await navigator.clipboard.writeText(message.content);
    setCopied(message.id);
    window.setTimeout(() => setCopied(null), 1500);
  };

  const listen = (message: Message) => {
    const utterance = new SpeechSynthesisUtterance(message.content.replace(/[#>*_`\n]/g, ' '));
    utterance.lang = 'en-IN';
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  };

  const toggleListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Voice input is not supported in this browser.');
      return;
    }
    if (listening) return setListening(false);
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.onresult = (event: any) => setInput(event.results[0][0].transcript);
    recognition.onend = () => setListening(false);
    recognition.onerror = () => setError('Voice input could not be started.');
    recognition.start();
    setListening(true);
  };

  const starter = (prompt: string) => sendMessage(prompt);

  return (
    <section className="flex h-full min-h-0 flex-col bg-[#f7f8fc]">
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto w-full max-w-4xl px-4 py-5 sm:px-8 sm:py-8">
          {messages.length === 0 && !loading ? (
            <div className="mx-auto flex min-h-[62vh] max-w-3xl flex-col items-center justify-center text-center">
              <div className="relative mb-6 flex h-20 w-20 items-center justify-center rounded-[28px] bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-xl shadow-indigo-200">
                <Sparkles size={34} />
                <span className="absolute -right-1 -top-1 h-4 w-4 rounded-full border-4 border-[#f7f8fc] bg-emerald-400" />
              </div>
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-indigo-500">Your AI companion</p>
              <h2 className="mt-3 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">SĀRTHI</h2>
              <p className="mt-3 max-w-xl text-lg leading-relaxed text-slate-500">Learn, translate, understand and explore Sanskrit through conversation.</p>
              <div className="mt-10 grid w-full gap-3 sm:grid-cols-2">
                {STARTERS.map(prompt => (
                  <button key={prompt} onClick={() => starter(prompt)} className="group flex items-center justify-between rounded-2xl border border-indigo-100 bg-indigo-50/70 px-4 py-3.5 text-left text-sm font-medium text-slate-700 shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-200 hover:bg-white hover:shadow-md">
                    {prompt}<ChevronRight size={16} className="text-indigo-300 transition group-hover:text-indigo-500" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6 pb-8">
              {messages.map((message: Message) => (
                <article key={message.id} className={`flex gap-3 sm:gap-4 ${message.role === 'user' ? 'justify-end' : ''}`}>
                  {message.role === 'assistant' && <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-sm"><Bot size={17} /></div>}
                  <div className={`min-w-0 max-w-[88%] sm:max-w-[78%] ${message.role === 'user' ? 'order-first' : ''}`}>
                    {message.role === 'assistant' && <div className="mb-2 flex items-center gap-2 px-1 text-[11px] font-semibold text-slate-400"><span>SĀRTHI</span>{message.intent && <span className="rounded-full bg-indigo-50 px-2 py-0.5 text-indigo-500">{message.intent}</span>}</div>}
                    <div className={`rounded-2xl px-4 py-3.5 shadow-sm ${message.role === 'user' ? 'rounded-br-md border border-indigo-100 bg-indigo-50 text-slate-800' : 'rounded-bl-md border border-slate-200 bg-white text-slate-700'}`}>
                      <Markdown>{message.content}</Markdown>
                    </div>
                    {message.role === 'assistant' && (
                      <div className="mt-2 flex items-center gap-1 px-1">
                        <button onClick={() => copyMessage(message)} className="rounded-lg p-1.5 text-slate-400 hover:bg-white hover:text-indigo-600" aria-label="Copy response">{copied === message.id ? <Check size={15} /> : <Copy size={15} />}</button>
                        <button onClick={() => listen(message)} className="rounded-lg p-1.5 text-slate-400 hover:bg-white hover:text-indigo-600" aria-label="Listen"><Volume2 size={15} /></button>
                        <button onClick={() => sendMessage('Explain that more simply.')} className="rounded-lg p-1.5 text-slate-400 hover:bg-white hover:text-indigo-600" aria-label="Explain simpler"><Headphones size={15} /></button>
                        <button onClick={() => sendMessage(message.content)} className="rounded-lg p-1.5 text-slate-400 hover:bg-white hover:text-indigo-600" aria-label="Regenerate"><Sparkles size={15} /></button>
                      </div>
                    )}
                  </div>
                  {message.role === 'user' && <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-200 text-xs font-bold text-slate-700">You</div>}
                </article>
              ))}

              {loading && (
                <div className="flex gap-4">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white"><Bot size={17} /></div>
                  <div className="min-w-0 max-w-[78%] rounded-2xl rounded-bl-md border border-slate-200 bg-white px-4 py-3.5 shadow-sm">
                    <div className="flex items-center gap-3 text-sm text-slate-600"><Loader2 size={17} className="animate-spin text-indigo-500" /><span>{thinking}</span></div>
                    {lastIntent && <p className="mt-2 text-[10px] text-slate-400">Intent: {lastIntent}</p>}
                  </div>
                </div>
              )}
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      <div className="border-t border-slate-200/80 bg-white/90 px-3 py-3 backdrop-blur sm:px-6">
        {error && <div className="mx-auto mb-2 max-w-4xl rounded-xl bg-rose-50 px-3 py-2 text-xs text-rose-600">{error}</div>}
        <div className="mx-auto flex max-w-4xl items-end gap-2 rounded-[22px] border border-slate-200 bg-white p-2 shadow-[0_12px_40px_rgba(36,42,67,0.08)] transition focus-within:border-indigo-300 focus-within:ring-4 focus-within:ring-indigo-50">
          <textarea value={input} onChange={event => setInput(event.target.value)} onKeyDown={event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); sendMessage(); } }} rows={1} placeholder="Ask SĀRTHI anything about Sanskrit..." className="max-h-32 min-h-11 flex-1 resize-none bg-transparent px-3 py-2.5 text-sm font-medium text-slate-600 outline-none placeholder:text-slate-400" />
          <button onClick={toggleListening} className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition ${listening ? 'bg-indigo-100 text-indigo-600' : 'text-slate-500 hover:bg-slate-100 hover:text-indigo-600'}`} aria-label="Voice input">{listening ? <MicOff size={18} /> : <Mic size={18} />}</button>
          <button onClick={() => sendMessage()} disabled={loading || !input.trim()} className="btn-primary flex h-11 w-11 shrink-0 items-center justify-center rounded-xl" aria-label="Send message"><Send size={17} /></button>
        </div>
        <p className="mx-auto mt-2 max-w-4xl text-center text-[10px] text-slate-400">Enter to send · Shift + Enter for a new line · Local-first</p>
      </div>
    </section>
  );
}
