import React, { useState } from 'react';

interface ChatInputProps {
  onSubmit: (query: string, functionName: string) => void;
  loading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState('');
  const [functionName, setFunctionName] = useState('');

  const quickScenarios = [
    { label: '⚡ Concurrency Throttling', text: 'my payment-processor-prod function is being throttled under peak load', func: 'payment-processor-prod' },
    { label: '❄️ Cold Start Latency', text: 'image-resizer-prod has severe 8-second cold starts during batch processing', func: 'image-resizer-prod' },
    { label: '💥 Out of Memory (OOM)', text: 'data-etl-prod killed abruptly with signal: killed, out of memory', func: 'data-etl-prod' },
    { label: '🚨 Runtime KeyError', text: 'notification-service-dev throws KeyError: user_id in handler', func: 'notification-service-dev' },
  ];

  const handleQuickSelect = (text: string, func: string) => {
    setQuery(text);
    setFunctionName(func);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    onSubmit(query.trim(), functionName.trim() || 'target-lambda-func');
  };

  return (
    <div className="bg-[#161B22] border border-[#30363D] rounded-xl p-5 shadow-lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-[#8B949E] uppercase tracking-wider mb-2">
            Issue Description & Query
          </label>
          <textarea
            rows={3}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
            placeholder="Describe the Lambda anomaly or error (e.g. 'function is throttled with 429 rate exceeded errors')..."
            className="w-full bg-[#0D1117] border border-[#30363D] rounded-lg px-4 py-3 text-sm text-[#C9D1D9] focus:outline-none focus:border-[#FF9900] transition placeholder-[#484F58] resize-none"
          />
        </div>

        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="w-full sm:w-1/2">
            <input
              type="text"
              value={functionName}
              onChange={(e) => setFunctionName(e.target.value)}
              disabled={loading}
              placeholder="Lambda Function Name (optional)"
              className="w-full bg-[#0D1117] border border-[#30363D] rounded-lg px-3.5 py-2 text-xs text-[#C9D1D9] focus:outline-none focus:border-[#FF9900] transition placeholder-[#484F58]"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="w-full sm:w-auto px-6 py-2.5 bg-[#FF9900] hover:bg-[#E68A00] disabled:bg-[#484F58] text-[#0D1117] font-bold text-xs uppercase tracking-wider rounded-lg transition flex items-center justify-center space-x-2 shadow"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-[#0D1117]" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Evaluating...</span>
              </>
            ) : (
              <span>Start Diagnosis</span>
            )}
          </button>
        </div>

        <div className="pt-2 border-t border-[#21262D]">
          <span className="text-[11px] text-[#8B949E] block mb-2 font-medium">Quick Scenarios:</span>
          <div className="flex flex-wrap gap-2">
            {quickScenarios.map((sc, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleQuickSelect(sc.text, sc.func)}
                disabled={loading}
                className="text-xs bg-[#21262D] hover:bg-[#30363D] text-[#C9D1D9] border border-[#30363D] px-2.5 py-1 rounded-md transition text-left"
              >
                {sc.label}
              </button>
            ))}
          </div>
        </div>
      </form>
    </div>
  );
};
