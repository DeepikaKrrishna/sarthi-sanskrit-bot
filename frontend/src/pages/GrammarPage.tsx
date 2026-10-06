import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ArrowLeft, ChevronRight } from 'lucide-react';

export function GrammarPage() {
  const [topics, setTopics] = useState<any[]>([]);
  const [active, setActive] = useState<any | null>(null);
  const [answer, setAnswer] = useState('');
  const [showResult, setShowResult] = useState(false);

  useEffect(() => { api.grammarTopics().then(setTopics).catch(() => {}); }, []);

  if (active) {
    const correct = answer === active.practice?.answer;
    return (
      <div className="h-full overflow-y-auto">
        <div className="max-w-2xl mx-auto px-4 py-8">
          <button onClick={() => { setActive(null); setAnswer(''); setShowResult(false); }}
            className="flex items-center gap-1 text-sm text-ink-500 hover:text-saffron-600 mb-6">
            <ArrowLeft size={16} /> All Topics
          </button>
          <h2 className="text-2xl font-bold text-ink-800 mb-4">{active.title}</h2>
          <p className="text-sm text-ink-700 leading-relaxed mb-6">{active.explanation}</p>

          <div className="space-y-2 mb-8">
            <h3 className="text-sm font-semibold text-ink-600 mb-2">Examples</h3>
            {active.examples?.map((ex: any, i: number) => (
              <div key={i} className="px-4 py-3 rounded-xl bg-white border border-ink-100">
                <div className="flex items-baseline gap-3">
                  <span className="font-semibold text-saffron-700">{ex.sanskrit}</span>
                  <span className="text-ink-500 text-sm">{ex.english}</span>
                </div>
                {ex.note && <p className="text-xs text-ink-400 mt-1">{ex.note}</p>}
              </div>
            ))}
          </div>

          {active.practice && (
            <div className="bg-white border border-ink-100 rounded-2xl p-5">
              <h3 className="font-semibold text-ink-700 mb-3">Practice</h3>
              <p className="text-sm text-ink-700 mb-3">{active.practice.question}</p>
              <div className="space-y-2">
                {active.practice.options.map((o: string) => (
                  <button key={o} onClick={() => { setAnswer(o); setShowResult(true); }}
                    disabled={showResult}
                    className={`w-full text-left px-4 py-2.5 rounded-xl text-sm border transition-colors
                      ${showResult && o === active.practice.answer ? 'border-leaf-500 bg-green-50 text-leaf-600 font-medium' :
                        showResult && o === answer && o !== active.practice.answer ? 'border-red-300 bg-red-50 text-red-600' :
                        'border-ink-200 hover:border-saffron-300'}`}>
                    {o}
                  </button>
                ))}
              </div>
              {showResult && (
                <p className={`mt-3 text-sm ${correct ? 'text-leaf-600' : 'text-red-600'}`}>
                  {correct ? 'Correct!' : `The answer is: ${active.practice.answer}`}
                  {active.practice.explanation && <span className="block text-ink-500 mt-1">{active.practice.explanation}</span>}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-ink-800 mb-1">Sanskrit Grammar</h2>
        <p className="text-sm text-ink-500 mb-6">Explore grammar topics with examples and practice</p>
        <div className="space-y-3">
          {topics.map(t => (
            <button key={t.id} onClick={() => setActive(t)}
              className="w-full flex items-center justify-between px-5 py-4 rounded-2xl bg-white border border-ink-100 hover:border-saffron-300 shadow-sm transition-colors text-left">
              <span className="text-sm font-semibold text-ink-700">{t.title}</span>
              <ChevronRight size={18} className="text-ink-300" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
