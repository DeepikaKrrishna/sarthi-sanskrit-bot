import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { RotateCcw, Trophy, ArrowRight, Check, X } from 'lucide-react';

interface QuizStats {
  totalAttempted: number;
  totalCorrect: number;
  sessions: number;
}

function loadStats(): QuizStats {
  try { return JSON.parse(localStorage.getItem('sarthi_quiz_stats') || '{}') as QuizStats; }
  catch { return { totalAttempted: 0, totalCorrect: 0, sessions: 0 }; }
}
function saveStats(s: QuizStats) { localStorage.setItem('sarthi_quiz_stats', JSON.stringify(s)); }

export function QuizPage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState('');
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [finished, setFinished] = useState(false);
  const [stats, setStats] = useState<QuizStats>(loadStats);
  const [loading, setLoading] = useState(true);

  const fetchQuiz = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.quiz(10);
      setQuestions(data);
    } catch { setQuestions([]); }
    setIdx(0); setSelected(''); setAnswered(false); setScore(0); setFinished(false);
    setLoading(false);
  }, []);

  useEffect(() => { fetchQuiz(); }, [fetchQuiz]);

  const q = questions[idx];

  const handleAnswer = (opt: string) => {
    if (answered) return;
    setSelected(opt);
    setAnswered(true);
    const correct = opt === q.answer;
    if (correct) setScore(s => s + 1);
  };

  const next = () => {
    if (idx + 1 >= questions.length) {
      const s: QuizStats = {
        totalAttempted: (stats.totalAttempted || 0) + questions.length,
        totalCorrect: (stats.totalCorrect || 0) + score + (selected === q?.answer ? 0 : 0),
        sessions: (stats.sessions || 0) + 1,
      };
      // re-calc since score already includes current
      s.totalCorrect = (stats.totalCorrect || 0) + score;
      saveStats(s);
      setStats(s);
      setFinished(true);
    } else {
      setIdx(i => i + 1);
      setSelected('');
      setAnswered(false);
    }
  };

  if (loading) return <div className="flex items-center justify-center h-full text-ink-400 text-sm">Loading quiz...</div>;

  if (finished) {
    const pct = questions.length ? Math.round((score / questions.length) * 100) : 0;
    return (
      <div className="h-full overflow-y-auto">
        <div className="max-w-md mx-auto px-4 py-16 text-center">
          <div className="w-16 h-16 rounded-full bg-saffron-100 text-saffron-600 flex items-center justify-center mx-auto mb-4">
            <Trophy size={28} />
          </div>
          <h2 className="text-2xl font-bold text-ink-800 mb-2">Quiz Complete</h2>
          <p className="text-4xl font-bold text-saffron-600 mb-1">{score}/{questions.length}</p>
          <p className="text-sm text-ink-500 mb-6">{pct}% accuracy</p>

          <div className="bg-white rounded-2xl border border-ink-100 p-5 mb-6 text-left space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-ink-500">Questions answered</span><span className="font-medium">{questions.length}</span></div>
            <div className="flex justify-between"><span className="text-ink-500">Correct</span><span className="font-medium text-leaf-600">{score}</span></div>
            <div className="flex justify-between"><span className="text-ink-500">Wrong</span><span className="font-medium text-red-500">{questions.length - score}</span></div>
            <hr className="border-ink-100" />
            <div className="flex justify-between"><span className="text-ink-500">All-time attempted</span><span className="font-medium">{stats.totalAttempted}</span></div>
            <div className="flex justify-between"><span className="text-ink-500">All-time correct</span><span className="font-medium">{stats.totalCorrect}</span></div>
            <div className="flex justify-between"><span className="text-ink-500">Sessions</span><span className="font-medium">{stats.sessions}</span></div>
          </div>

          <button onClick={fetchQuiz}
            className="btn-primary inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium">
            <RotateCcw size={16} /> Take Another Quiz
          </button>
        </div>
      </div>
    );
  }

  if (!q) return <div className="flex items-center justify-center h-full text-ink-400 text-sm">No questions available.</div>;

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-xl mx-auto px-4 py-8">
        {/* progress */}
        <div className="flex items-center justify-between mb-6">
          <span className="text-xs text-ink-400">Question {idx + 1} of {questions.length}</span>
          <span className="text-xs text-ink-400">Score: {score}</span>
        </div>
        <div className="w-full h-1.5 rounded-full bg-ink-100 mb-8">
          <div className="h-full rounded-full bg-saffron-500 transition-all" style={{ width: `${((idx + 1) / questions.length) * 100}%` }} />
        </div>

        {/* question */}
        <div className="bg-white rounded-2xl border border-ink-100 shadow-sm p-6 mb-4">
          {q.category && <span className="inline-block px-2 py-0.5 rounded bg-saffron-50 text-saffron-600 text-xs mb-3">{q.category}</span>}
          <h3 className="text-lg font-semibold text-ink-800 mb-5">{q.question}</h3>

          <div className="space-y-2.5">
            {q.options.map((o: string, i: number) => {
              const letter = String.fromCharCode(65 + i);
              const isCorrect = o === q.answer;
              const isSelected = o === selected;
              let cls = 'border-ink-200 hover:border-saffron-300';
              if (answered) {
                if (isCorrect) cls = 'border-leaf-500 bg-green-50';
                else if (isSelected) cls = 'border-red-300 bg-red-50';
                else cls = 'border-ink-100 opacity-60';
              }
              return (
                <button
                  key={o}
                  onClick={() => handleAnswer(o)}
                  disabled={answered}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-sm text-left transition-colors ${cls}`}
                >
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium shrink-0
                    ${answered && isCorrect ? 'bg-leaf-500 text-white' : answered && isSelected ? 'bg-red-400 text-white' : 'bg-ink-100 text-ink-600'}`}>
                    {answered && isCorrect ? <Check size={14} /> : answered && isSelected ? <X size={14} /> : letter}
                  </span>
                  <span className={answered && isCorrect ? 'font-medium text-leaf-600' : answered && isSelected && !isCorrect ? 'text-red-600' : 'text-ink-700'}>
                    {o}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* explanation */}
        {answered && (
          <div className={`rounded-xl px-4 py-3 text-sm mb-4 ${selected === q.answer ? 'bg-green-50 border border-green-200 text-leaf-600' : 'bg-red-50 border border-red-200 text-red-600'}`}>
            <p className="font-medium mb-1">{selected === q.answer ? 'Correct!' : `Incorrect — the answer is: ${q.answer}`}</p>
            {q.explanation && <p className="text-ink-600">{q.explanation}</p>}
          </div>
        )}

        {answered && (
          <button onClick={next}
            className="btn-primary flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium">
            {idx + 1 >= questions.length ? 'See Results' : 'Next Question'} <ArrowRight size={16} />
          </button>
        )}
      </div>
    </div>
  );
}
