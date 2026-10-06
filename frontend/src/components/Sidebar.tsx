import type { Page } from '../App';
import { BookOpen, Brain, Languages, MessageCircle, MessageSquarePlus, Mic, ScrollText, Trash2, X } from 'lucide-react';

const NAV: { id: Page; label: string; icon: typeof MessageCircle }[] = [
  { id: 'chat', label: 'Chat with SĀRTHI', icon: MessageCircle },
  { id: 'learn', label: 'Learning path', icon: BookOpen },
  { id: 'grammar', label: 'Grammar', icon: Languages },
  { id: 'shlokas', label: 'Shlokas', icon: ScrollText },
  { id: 'quiz', label: 'Practice quiz', icon: Brain },
  { id: 'voice', label: 'Voice studio', icon: Mic },
];

export function Sidebar({ page, setPage, open, toggle, chat }: {
  page: Page;
  setPage: (p: Page) => void;
  open: boolean;
  toggle: () => void;
  chat: any;
}) {
  const navigate = (next: Page) => {
    setPage(next);
    if (window.innerWidth < 768) toggle();
  };

  return (
    <>
      {open && <div className="md:hidden fixed inset-0 bg-slate-950/40 z-30" onClick={toggle} />}
      <aside className={`fixed md:static z-40 top-0 left-0 h-full w-[280px] flex flex-col bg-[#171a28] text-slate-100 transition-transform duration-200 ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:w-0 md:overflow-hidden'}`}>
        <div className="flex items-center justify-between px-5 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-lg shadow-indigo-950/40">
              <span className="text-lg font-bold text-white">S</span>
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-wide text-white">SĀRTHI</h1>
              <p className="text-[11px] text-slate-400">Sanskrit AI companion</p>
            </div>
          </div>
          <button onClick={toggle} className="rounded-lg p-2 text-slate-400 hover:bg-white/10 hover:text-white md:hidden" aria-label="Close sidebar"><X size={19} /></button>
        </div>

        <div className="px-4">
          <button onClick={() => { chat.newChat(); navigate('chat'); }} className="btn-primary flex w-full items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold">
            <MessageSquarePlus size={17} /> New conversation
          </button>
        </div>

        <nav className="mt-5 flex-1 space-y-1 overflow-y-auto px-3">
          {NAV.map(({ id, label, icon: Icon }) => (
            <button key={id} onClick={() => navigate(id)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm transition ${page === id ? 'bg-white/10 text-white' : 'text-slate-400 hover:bg-white/[0.06] hover:text-white'}`}>
              <Icon size={18} className={page === id ? 'text-indigo-300' : ''} /> {label}
            </button>
          ))}

          <div className="mt-5 border-t border-white/10 pt-5">
            <div className="mb-2 flex items-center justify-between px-3">
              <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">Recent chats</span>
              {chat.conversations.length > 0 && <button onClick={chat.clearAll} className="text-[10px] text-slate-500 hover:text-rose-300">Clear</button>}
            </div>
            {chat.conversations.slice(0, 10).map((conversation: any) => (
              <div key={conversation.id} className="group flex items-center">
                <button onClick={() => { chat.setActiveId(conversation.id); navigate('chat'); }} className={`min-w-0 flex-1 rounded-lg px-3 py-2 text-left text-xs transition ${chat.activeId === conversation.id ? 'bg-white/10 text-indigo-200' : 'text-slate-500 hover:bg-white/[0.05] hover:text-slate-200'}`}>
                  <span className="block truncate">{conversation.title}</span>
                </button>
                <button onClick={() => chat.deleteConversation(conversation.id)} className="mr-1 rounded-lg p-1.5 text-slate-600 opacity-0 transition hover:text-rose-300 group-hover:opacity-100" aria-label="Delete conversation"><Trash2 size={13} /></button>
              </div>
            ))}
          </div>
        </nav>

        <div className="border-t border-white/10 px-5 py-4">
          <p className="text-xs font-medium text-slate-300">Local-first learning</p>
          <p className="mt-1 text-[10px] text-slate-500">Ollama optional · tools always available</p>
        </div>
      </aside>
    </>
  );
}
