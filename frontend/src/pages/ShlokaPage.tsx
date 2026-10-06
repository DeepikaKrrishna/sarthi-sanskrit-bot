import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Search, ArrowLeft } from 'lucide-react';

export function ShlokaPage() {
  const [shlokas, setShlokas] = useState<any[]>([]);
  const [active, setActive] = useState<any | null>(null);
  const [query, setQuery] = useState('');

  useEffect(() => { api.shlokas().then(setShlokas).catch(() => {}); }, []);

  const filtered = query.trim()
    ? shlokas.filter(s =>
        s.sanskrit.includes(query) ||
        s.transliteration.toLowerCase().includes(query.toLowerCase()) ||
        s.meaning.toLowerCase().includes(query.toLowerCase()) ||
        (s.source || '').toLowerCase().includes(query.toLowerCase())
      )
    : shlokas;

  if (active) {
    return (
      <div className="h-full overflow-y-auto">
        <div className="max-w-2xl mx-auto px-4 py-8">
          <button onClick={() => setActive(null)}
            className="flex items-center gap-1 text-sm text-ink-500 hover:text-saffron-600 mb-6">
            <ArrowLeft size={16} /> All Shlokas
          </button>
          <div className="bg-white rounded-2xl border border-ink-100 shadow-sm overflow-hidden">
            <div className="bg-saffron-50 px-6 py-8 text-center border-b border-saffron-100">
              <p className="text-xl font-semibold text-ink-800 leading-relaxed" style={{ fontFamily: '"Noto Sans Devanagari", sans-serif' }}>
                {active.sanskrit}
              </p>
              <p className="text-sm text-ink-500 mt-3 italic">{active.transliteration}</p>
            </div>
            <div className="px-6 py-6 space-y-5">
              <div>
                <h3 className="text-xs font-semibold text-ink-400 uppercase tracking-wide mb-1">Meaning</h3>
                <p className="text-sm text-ink-700">{active.meaning}</p>
              </div>
              <div>
                <h3 className="text-xs font-semibold text-ink-400 uppercase tracking-wide mb-1">Explanation</h3>
                <p className="text-sm text-ink-600 leading-relaxed">{active.explanation}</p>
              </div>
              {active.source && (
                <div>
                  <h3 className="text-xs font-semibold text-ink-400 uppercase tracking-wide mb-1">Source</h3>
                  <p className="text-sm text-ink-500 italic">{active.source}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-ink-800 mb-1">Sanskrit Shlokas</h2>
        <p className="text-sm text-ink-500 mb-5">A collection of verses with meanings and explanations</p>

        <div className="relative mb-6">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-400" />
          <input
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search shlokas by text, meaning, or source..."
            className="w-full pl-9 pr-4 py-2.5 rounded-xl border border-ink-200 text-sm focus:outline-none focus:border-saffron-400 focus:ring-2 focus:ring-saffron-100"
          />
        </div>

        <div className="space-y-3">
          {filtered.length === 0 && (
            <p className="text-sm text-ink-400 text-center py-8">No shlokas match your search.</p>
          )}
          {filtered.map(s => (
            <button key={s.id} onClick={() => setActive(s)}
              className="w-full text-left px-5 py-4 rounded-2xl bg-white border border-ink-100 hover:border-saffron-300 shadow-sm transition-colors">
              <p className="font-semibold text-ink-700 mb-1" style={{ fontFamily: '"Noto Sans Devanagari", sans-serif' }}>
                {s.sanskrit}
              </p>
              <p className="text-sm text-ink-500">{s.meaning}</p>
              {s.source && <p className="text-xs text-ink-400 mt-1 italic">{s.source}</p>}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
