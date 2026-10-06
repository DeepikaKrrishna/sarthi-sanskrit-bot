import { Check, Loader2 } from 'lucide-react';

const STEPS = ['Analyze', 'Choose', 'Take Action'];

export function ActStatus({ stage, intent }: { stage: number; intent?: string }) {
  return (
    <div className="flex items-center gap-4 px-3 py-2 rounded-lg bg-saffron-50 border border-saffron-200 text-xs">
      <span className="font-semibold text-saffron-700 tracking-wide">ACT</span>
      {STEPS.map((s, i) => (
        <span key={s} className="flex items-center gap-1">
          {i < stage ? (
            <Check size={13} className="text-leaf-500" />
          ) : i === stage ? (
            <Loader2 size={13} className="text-saffron-500 animate-spin" />
          ) : (
            <span className="w-3 h-3 rounded-full border border-ink-300" />
          )}
          <span className={i <= stage ? 'text-ink-700' : 'text-ink-400'}>{s}</span>
        </span>
      ))}
      {intent && stage >= 3 && (
        <span className="ml-auto text-ink-400">Intent: {intent}</span>
      )}
    </div>
  );
}
