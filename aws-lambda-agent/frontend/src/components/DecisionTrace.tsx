import React from 'react';
import { DiagnosticStep } from '../types';

interface DecisionTraceProps {
  steps: DiagnosticStep[];
  deciderMode: string;
}

export const DecisionTrace: React.FC<DecisionTraceProps> = ({ steps, deciderMode }) => {
  const toolLabels: Record<string, string> = {
    get_cloudwatch_logs: 'CloudWatch Logs',
    get_lambda_metrics: 'Lambda Metrics',
    get_lambda_config: 'Lambda Configuration',
    get_aws_health_events: 'AWS Health Events',
  };

  return (
    <div className="bg-[#161B22] border border-[#30363D] rounded-xl p-5 shadow-lg flex flex-col h-full">
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-[#21262D]">
        <div className="flex items-center space-x-2">
          <span className="text-lg">🧠</span>
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Decision Trace
          </h2>
        </div>
        <span className="text-[11px] font-mono text-[#8B949E] bg-[#0D1117] border border-[#30363D] px-2 py-0.5 rounded">
          {deciderMode === 'strands-decider-2b' ? 'Strands Decider 2B' : 'Decider 2B Pattern'}
        </span>
      </div>

      <div className="space-y-4 flex-1">
        {steps.map((step) => {
          const confPercent = Math.round(step.confidence * 100);
          const barColor =
            confPercent >= 85 ? 'bg-[#3FB950]' : confPercent >= 70 ? 'bg-[#D29922]' : 'bg-[#F85149]';

          return (
            <div
              key={step.step}
              className="bg-[#0D1117] border border-[#30363D] rounded-lg p-3.5 relative overflow-hidden transition-all hover:border-[#484F58]"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className="w-5 h-5 rounded-full bg-[#FF9900] text-[#0D1117] text-xs font-bold flex items-center justify-center">
                    {step.step}
                  </span>
                  <span className="font-mono text-xs font-semibold text-white">
                    {toolLabels[step.tool_selected] || step.tool_selected}
                  </span>
                </div>
                <span className="font-mono text-xs font-bold text-[#C9D1D9]">
                  {confPercent}% confidence
                </span>
              </div>

              {/* Confidence progress bar */}
              <div className="w-full bg-[#21262D] rounded-full h-1.5 mb-2.5 overflow-hidden">
                <div
                  className={`h-1.5 rounded-full ${barColor} transition-all duration-500`}
                  style={{ width: `${confPercent}%` }}
                ></div>
              </div>

              <p className="text-xs text-[#8B949E] leading-relaxed mb-3">
                {step.reasoning}
              </p>

              {/* Probabilities breakdown */}
              {step.probabilities && Object.keys(step.probabilities).length > 0 && (
                <div className="pt-2 border-t border-[#21262D]">
                  <span className="text-[10px] text-[#484F58] uppercase font-mono block mb-1">
                    Option distribution:
                  </span>
                  <div className="grid grid-cols-2 gap-1.5 text-[11px] font-mono">
                    {Object.entries(step.probabilities).map(([tool, prob]) => (
                      <div
                        key={tool}
                        className={`flex items-center justify-between px-2 py-0.5 rounded ${
                          tool === step.tool_selected ? 'bg-[#161B22] text-[#FF9900] border border-[#FF9900]/30 font-semibold' : 'text-[#8B949E]'
                        }`}
                      >
                        <span className="truncate pr-1">{toolLabels[tool] || tool}</span>
                        <span>{Math.round(prob * 100)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
