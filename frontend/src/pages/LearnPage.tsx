import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { BookOpen, Check, ChevronRight, ArrowLeft } from 'lucide-react';

function getProgress(): Record<number, boolean> {
  try { return JSON.parse(localStorage.getItem('sarthi_lesson_progress') || '{}'); } catch { return {}; }
}
function setProgress(id: number) {
  const p = getProgress(); p[id] = true;
  localStorage.setItem('sarthi_lesson_progress', JSON.stringify(p));
}

export function LearnPage() {
  const [lessons, setLessons] = useState<any[]>([]);
  const [active, setActive] = useState<any | null>(null);
  const [answer, setAnswer] = useState('');
  const [showResult, setShowResult] = useState(false);
  const progress = getProgress();

  useEffect(() => { api.lessons().then(setLessons).catch(() => {}); }, []);

  if (active) {
    const correct = answer === active.practice?.answer;
    return (
      <div className="h-full overflow-y-auto">
        <div className="max-w-2xl mx-auto px-4 py-8">
          <button onClick={() => { setActive(null); setAnswer(''); setShowResult(false); }}
            className="flex items-center gap-1 text-sm text-ink-500 hover:text-saffron-600 mb-6">
            <ArrowLeft size={16} /> All Lessons
          </button>
          <h2 className="text-2xl font-bold text-ink-800 mb-1">Lesson {active.id}: {active.title}</h2>
          <span className="inline-block px-2 py-0.5 rounded bg-saffron-100 text-saffron-700 text-xs mb-6">{active.level}</span>
          <p className="text-sm text-ink-700 leading-relaxed mb-6">{active.content}</p>

          {active.examples?.length > 0 && (
            <div className="space-y-2 mb-8">
              <h3 className="text-sm font-semibold text-ink-600 mb-2">Examples</h3>
              {active.examples.map((ex: any, i: number) => (
                <div key={i} className="flex items-baseline gap-3 px-4 py-2.5 rounded-xl bg-white border border-ink-100">
                  <span className="font-semibold text-saffron-700">{ex.sanskrit}</span>
                  <span className="text-ink-500 text-sm">— {ex.english}</span>
                </div>
              ))}
            </div>
          )}

          {active.practice && (
            <div className="bg-white border border-ink-100 rounded-2xl p-5">
              <h3 className="font-semibold text-ink-700 mb-3">Practice</h3>
              <p className="text-sm text-ink-700 mb-3">{active.practice.question}</p>
              <div className="space-y-2">
                {active.practice.options.map((o: string) => (
                  <button key={o} onClick={() => { setAnswer(o); setShowResult(true); setProgress(active.id); }}
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
                  {correct ? 'Correct!' : `Not quite. The answer is: ${active.practice.answer}`}
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
        <h2 className="text-2xl font-bold text-ink-800 mb-1">Learn Sanskrit</h2>
        <p className="text-sm text-ink-500 mb-6">Guided lessons from basics to sentence construction</p>
        <div className="space-y-3">
          {lessons.map(l => (
            <button key={l.id} onClick={() => setActive(l)}
              className="w-full flex items-center gap-4 px-5 py-4 rounded-2xl bg-white border border-ink-100 hover:border-saffron-300 shadow-sm transition-colors text-left">
              <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0
                ${progress[l.id] ? 'bg-green-100 text-leaf-600' : 'bg-saffron-100 text-saffron-600'}`}>
                {progress[l.id] ? <Check size={18} /> : <BookOpen size={18} />}
              </div>
              <div className="flex-1">
                <span className="text-sm font-semibold text-ink-700">Lesson {l.id}: {l.title}</span>
                <span className="block text-xs text-ink-400 mt-0.5">{l.level}</span>
              </div>
              <ChevronRight size={18} className="text-ink-300" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
