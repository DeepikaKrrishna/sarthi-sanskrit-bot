import { useState, useRef, useCallback } from 'react';
import { Mic, MicOff, Volume2, Send, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import { Markdown } from '../components/Markdown';

const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
const hasSpeech = !!SpeechRecognition;
const hasTTS = 'speechSynthesis' in window;

export function VoicePage() {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const recogRef = useRef<any>(null);

  const startRecording = useCallback(() => {
    if (!hasSpeech) return;
    const recog = new SpeechRecognition();
    recog.lang = 'en-US';
    recog.interimResults = true;
    recog.continuous = false;

    recog.onresult = (e: any) => {
      let text = '';
      for (let i = 0; i < e.results.length; i++) {
        text += e.results[i][0].transcript;
      }
      setTranscript(text);
    };
    recog.onerror = () => setRecording(false);
    recog.onend = () => setRecording(false);

    recogRef.current = recog;
    recog.start();
    setRecording(true);
  }, []);

  const stopRecording = useCallback(() => {
    recogRef.current?.stop();
    setRecording(false);
  }, []);

  const sendToChat = async () => {
    if (!transcript.trim() || loading) return;
    setLoading(true);
    try {
      const res = await api.chat({
        message: transcript,
        conversation_history: [],
        learner_context: { level: 'beginner', language: 'en' },
      });
      setResponse(res.response || 'No response');
    } catch {
      setResponse('Could not reach the backend. Make sure the server is running.');
    }
    setLoading(false);
  };

  const speak = (text: string) => {
    if (!hasTTS || speaking) return;
    // strip markdown bold/etc for cleaner speech
    const clean = text.replace(/\*\*/g, '').replace(/[#_>`]/g, '');
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = 'en-US';
    utter.rate = 0.9;
    utter.onstart = () => setSpeaking(true);
    utter.onend = () => setSpeaking(false);
    utter.onerror = () => setSpeaking(false);
    speechSynthesis.speak(utter);
  };

  const stopSpeaking = () => {
    speechSynthesis.cancel();
    setSpeaking(false);
  };

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-ink-800 mb-1">Voice Studio</h2>
        <p className="text-sm text-ink-500 mb-8">Speak to SĀRTHI and hear responses read aloud</p>

        {/* Speech-to-Text */}
        <div className="bg-white rounded-2xl border border-ink-100 shadow-sm p-6 mb-6">
          <h3 className="font-semibold text-ink-700 mb-4">Speech to Text</h3>

          {!hasSpeech && (
            <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-amber-50 border border-amber-200 text-sm text-amber-700 mb-4">
              <AlertCircle size={18} className="shrink-0 mt-0.5" />
              <p>Your browser does not support speech recognition. Try Chrome or Edge for this feature.</p>
            </div>
          )}

          <div className="flex gap-3 mb-4">
            {!recording ? (
              <button onClick={startRecording} disabled={!hasSpeech}
                className="btn-primary flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium disabled:cursor-not-allowed">
                <Mic size={16} /> Start Recording
              </button>
            ) : (
              <button onClick={stopRecording}
                className="btn-danger flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium animate-pulse">
                <MicOff size={16} /> Stop Recording
              </button>
            )}
          </div>

          <div className="min-h-[60px] px-4 py-3 rounded-xl bg-ink-50 border border-ink-100 text-sm text-ink-700 mb-4">
            {transcript || <span className="text-ink-400">{recording ? 'Listening...' : 'Your speech will appear here'}</span>}
          </div>

          <div className="flex gap-2">
            <input
              value={transcript}
              onChange={e => setTranscript(e.target.value)}
              placeholder="Or type here to edit..."
              className="flex-1 px-4 py-2.5 rounded-xl border border-ink-200 text-sm focus:outline-none focus:border-saffron-400 focus:ring-2 focus:ring-saffron-100"
            />
            <button onClick={sendToChat} disabled={!transcript.trim() || loading}
              className="btn-primary flex h-[42px] w-[42px] items-center justify-center rounded-xl disabled:cursor-not-allowed">
              <Send size={16} />
            </button>
          </div>
        </div>

        {/* Response + TTS */}
        <div className="bg-white rounded-2xl border border-ink-100 shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-ink-700">SĀRTHI Response</h3>
            {response && hasTTS && (
              <button onClick={() => speaking ? stopSpeaking() : speak(response)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors
                  ${speaking ? 'bg-red-100 text-red-600 hover:bg-red-200' : 'bg-saffron-100 text-saffron-600 hover:bg-saffron-200'}`}>
                <Volume2 size={14} /> {speaking ? 'Stop' : 'Speak Response'}
              </button>
            )}
          </div>

          {!hasTTS && (
            <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-amber-50 border border-amber-200 text-sm text-amber-700 mb-4">
              <AlertCircle size={18} className="shrink-0 mt-0.5" />
              <p>Your browser does not support text-to-speech.</p>
            </div>
          )}

          <div className="min-h-[80px] px-4 py-3 rounded-xl bg-ink-50 border border-ink-100">
            {loading ? (
              <p className="text-sm text-ink-400 animate-pulse">Processing...</p>
            ) : response ? (
              <Markdown>{response}</Markdown>
            ) : (
              <p className="text-sm text-ink-400">The response will appear here after you send a message.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
