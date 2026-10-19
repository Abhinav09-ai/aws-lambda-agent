import React, { useState } from 'react';

interface DiagnosisCardProps {
  rootCause: string;
  explanation: string;
  fixRecommendation: string;
  fixCommands: string[];
  synthesisMode: string;
}

export const DiagnosisCard: React.FC<DiagnosisCardProps> = ({
  rootCause,
  explanation,
  fixRecommendation,
  fixCommands,
  synthesisMode,
}) => {
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);

  const copyToClipboard = (cmd: string, idx: number) => {
    navigator.clipboard.writeText(cmd);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  const isBedrock = synthesisMode === 'bedrock';

  return (
    <div className="bg-[#161B22] border border-[#30363D] rounded-xl p-6 shadow-xl space-y-6">
      {/* Root Cause Section */}
      <div className="border-l-4 border-[#F85149] pl-4 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase tracking-wider text-[#F85149] font-bold">
            Identified Root Cause
          </span>
          <span
            className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
              isBedrock
                ? 'bg-[#58A6FF]/10 text-[#58A6FF] border-[#58A6FF]/30'
                : 'bg-[#FF9900]/10 text-[#FF9900] border-[#FF9900]/30'
            }`}
          >
            {isBedrock ? 'Synthesized via Amazon Bedrock (Claude 3)' : 'Verified Diagnostic Template (Demo Mode)'}
          </span>
        </div>
        <h3 className="text-lg font-bold text-white tracking-wide">{rootCause}</h3>
        <p className="text-sm text-[#8B949E] leading-relaxed">{explanation}</p>
      </div>

      {/* Recommended Fix Section */}
      <div className="border-l-4 border-[#3FB950] pl-4 space-y-3">
        <span className="text-[11px] font-mono uppercase tracking-wider text-[#3FB950] font-bold">
          Recommended Safe Remediation
        </span>
        <p className="text-sm text-[#C9D1D9] leading-relaxed">{fixRecommendation}</p>

        {fixCommands && fixCommands.length > 0 && (
          <div className="space-y-2 pt-2">
            <span className="text-[11px] font-mono text-[#8B949E] block">
              Suggested AWS CLI commands (Read & Apply with Operator Review):
            </span>
            {fixCommands.map((cmd, idx) => (
              <div
                key={idx}
                className="bg-[#0D1117] border border-[#30363D] rounded-lg p-3 flex items-center justify-between font-mono text-xs group hover:border-[#FF9900]/50 transition"
              >
                <code className="text-[#FF9900] break-all select-all pr-4">{cmd}</code>
                <button
                  type="button"
                  onClick={() => copyToClipboard(cmd, idx)}
                  className="px-2.5 py-1 bg-[#21262D] hover:bg-[#30363D] text-[#C9D1D9] text-[11px] rounded transition flex items-center space-x-1 flex-shrink-0"
                >
                  {copiedIdx === idx ? (
                    <span className="text-[#3FB950] font-semibold">✓ Copied</span>
                  ) : (
                    <span>Copy</span>
                  )}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
