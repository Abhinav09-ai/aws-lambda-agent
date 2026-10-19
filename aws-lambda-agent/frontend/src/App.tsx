import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ChatInput } from './components/ChatInput';
import { DecisionTrace } from './components/DecisionTrace';
import { EvidencePanel } from './components/EvidencePanel';
import { DiagnosisCard } from './components/DiagnosisCard';
import { diagnose, getApiInfo } from './api';
import { DiagnoseResponse } from './types';

export const App: React.FC = () => {
  const [deciderMode, setDeciderMode] = useState<string>('fallback');
  const [synthesisMode, setSynthesisMode] = useState<string>('demo');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnoseResponse | null>(null);

  useEffect(() => {
    getApiInfo()
      .then((info) => {
        setDeciderMode(info.decider_mode);
        setSynthesisMode(info.synthesis_mode);
      })
      .catch((err) => {
        console.warn('API info fetch error:', err);
      });
  }, []);

  const handleDiagnose = async (query: string, functionName: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await diagnose(query, functionName);
      setResult(data);
      setDeciderMode(data.decider_mode);
      setSynthesisMode(data.synthesis_mode);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Diagnostic execution failed';
      setError(`Failed to reach agent backend: ${msg}. Make sure FastAPI is running on port 8000.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0D1117] text-[#C9D1D9] flex flex-col font-sans selection:bg-[#FF9900]/30 selection:text-[#FF9900]">
      <Header deciderMode={deciderMode} synthesisMode={synthesisMode} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        <ChatInput onSubmit={handleDiagnose} loading={loading} />

        {error && (
          <div className="bg-[#F85149]/10 border border-[#F85149]/40 rounded-xl p-4 text-xs font-mono text-[#F85149]">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="bg-[#161B22] border border-[#30363D] rounded-xl p-8 text-center space-y-4 shadow-lg animate-pulse">
            <div className="inline-block p-3 rounded-full bg-[#FF9900]/10 text-[#FF9900]">
              <svg className="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <div className="space-y-1">
              <h3 className="text-sm font-bold text-white tracking-wide">
                Strands Decider 2B is Evaluating Diagnostic Path
              </h3>
              <p className="text-xs text-[#8B949E]">
                Selecting optimal diagnostic tools and correlating telemetry signals...
              </p>
            </div>
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
              <DecisionTrace
                steps={result.decision_trace}
                deciderMode={result.decider_mode}
              />
              <EvidencePanel
                evidence={result.evidence}
                scenario={result.scenario_detected}
              />
            </div>

            <DiagnosisCard
              rootCause={result.root_cause}
              explanation={result.explanation}
              fixRecommendation={result.fix_recommendation}
              fixCommands={result.fix_commands}
              synthesisMode={result.synthesis_mode}
            />
          </div>
        )}
      </main>

      <footer className="border-t border-[#21262D] py-4 text-center text-xs text-[#484F58]">
        AWS Agent Experience Hackathon • Strands Decider 2B (#tool-selection) • Read-Only Diagnostic Architecture
      </footer>
    </div>
  );
};

export default App;
