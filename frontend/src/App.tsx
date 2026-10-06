import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatPage } from './pages/ChatPage';
import { LearnPage } from './pages/LearnPage';
import { GrammarPage } from './pages/GrammarPage';
import { ShlokaPage } from './pages/ShlokaPage';
import { QuizPage } from './pages/QuizPage';
import { VoicePage } from './pages/VoicePage';
import { useChatHistory } from './hooks/useChatHistory';

export type Page = 'chat' | 'learn' | 'grammar' | 'shlokas' | 'quiz' | 'voice';

export default function App() {
  const [page, setPage] = useState<Page>('chat');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const chat = useChatHistory();

  const renderPage = () => {
    switch (page) {
      case 'chat': return <ChatPage chat={chat} />;
      case 'learn': return <LearnPage />;
      case 'grammar': return <GrammarPage />;
      case 'shlokas': return <ShlokaPage />;
      case 'quiz': return <QuizPage />;
      case 'voice': return <VoicePage />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-ink-50">
      <Sidebar
        page={page}
        setPage={setPage}
        open={sidebarOpen}
        toggle={() => setSidebarOpen(p => !p)}
        chat={chat}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* mobile top bar */}
        <div className="md:hidden flex items-center gap-3 px-4 py-3 border-b border-ink-100 bg-white">
          <button onClick={() => setSidebarOpen(true)} className="text-ink-600">
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
          <span className="font-semibold text-saffron-700">SĀRTHI</span>
        </div>
        <div className="flex-1 overflow-hidden">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}
