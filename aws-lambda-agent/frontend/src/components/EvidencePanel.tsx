import React, { useState } from 'react';
import { Evidence } from '../types';

interface EvidencePanelProps {
  evidence: Evidence;
  scenario: string;
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({ evidence }) => {
  const [activeTab, setActiveTab] = useState<'logs' | 'metrics' | 'config' | 'health'>('logs');

  const logsData = evidence.get_cloudwatch_logs as { log_entries?: string[]; period?: string } | undefined;
  const metricsData = evidence.get_lambda_metrics as { metrics?: Record<string, number>; period?: string } | undefined;
  const configData = evidence.get_lambda_config as { config?: Record<string, unknown> } | undefined;
  const healthData = evidence.get_aws_health_events as { events?: Array<{ service?: string; status?: string; description?: string }> } | undefined;

  return (
    <div className="bg-[#161B22] border border-[#30363D] rounded-xl p-5 shadow-lg flex flex-col h-full">
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-[#21262D]">
        <div className="flex items-center space-x-2">
          <span className="text-lg">🔍</span>
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Gathered Evidence
          </h2>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 bg-[#0D1117] p-1 rounded-lg border border-[#30363D] text-xs font-mono">
          {(['logs', 'metrics', 'config', 'health'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-2.5 py-1 rounded transition uppercase ${
                activeTab === tab
                  ? 'bg-[#FF9900] text-[#0D1117] font-bold shadow'
                  : 'text-[#8B949E] hover:text-[#C9D1D9]'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {activeTab === 'logs' && (
          <div className="bg-[#0D1117] border border-[#30363D] rounded-lg p-3 font-mono text-xs text-[#3FB950] space-y-1 max-h-[360px] overflow-y-auto">
            <div className="text-[#8B949E] pb-1 border-b border-[#21262D] text-[11px]">
              CloudWatch Logs Stream • {logsData?.period || '15 min window'}
            </div>
            {logsData?.log_entries && logsData.log_entries.length > 0 ? (
              logsData.log_entries.map((log, i) => (
                <div key={i} className="leading-relaxed hover:bg-[#161B22]/50 px-1 rounded">
                  {log}
                </div>
              ))
            ) : (
              <div className="text-[#8B949E] italic py-4 text-center">No logs collected in this trace.</div>
            )}
          </div>
        )}

        {activeTab === 'metrics' && (
          <div className="grid grid-cols-2 gap-3">
            {metricsData?.metrics ? (
              Object.entries(metricsData.metrics).map(([key, val]) => {
                const isError = key.includes('error') && val > 0.05;
                const isThrottle = key.includes('throttle') && val > 0;
                const isBad = isError || isThrottle;

                return (
                  <div
                    key={key}
                    className={`bg-[#0D1117] border ${
                      isBad ? 'border-[#F85149]/40 bg-[#F85149]/5' : 'border-[#30363D]'
                    } rounded-lg p-3.5 flex flex-col justify-between`}
                  >
                    <span className="text-[11px] font-mono text-[#8B949E] uppercase truncate">
                      {key.replace(/_/g, ' ')}
                    </span>
                    <span
                      className={`text-xl font-mono font-bold mt-1 ${
                        isBad ? 'text-[#F85149]' : 'text-white'
                      }`}
                    >
                      {typeof val === 'number' && val < 1 && val > 0
                        ? `${Math.round(val * 100)}%`
                        : val.toLocaleString()}
                    </span>
                  </div>
                );
              })
            ) : (
              <div className="col-span-2 text-[#8B949E] italic py-8 text-center">
                Lambda metrics were not gathered in this diagnostic path.
              </div>
            )}
          </div>
        )}

        {activeTab === 'config' && (
          <div className="bg-[#0D1117] border border-[#30363D] rounded-lg overflow-hidden text-xs font-mono">
            {configData?.config ? (
              <table className="w-full text-left">
                <tbody>
                  {Object.entries(configData.config).map(([k, v], i) => (
                    <tr
                      key={k}
                      className={`border-b border-[#21262D] ${i % 2 === 0 ? 'bg-[#0D1117]' : 'bg-[#161B22]/30'}`}
                    >
                      <td className="py-2.5 px-3 text-[#8B949E]">{k}</td>
                      <td className="py-2.5 px-3 text-[#C9D1D9] font-semibold">{String(v)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-[#8B949E] italic py-8 text-center">
                Configuration was not retrieved.
              </div>
            )}
          </div>
        )}

        {activeTab === 'health' && (
          <div className="space-y-2">
            {healthData?.events && healthData.events.length > 0 ? (
              healthData.events.map((ev, i) => (
                <div key={i} className="bg-[#0D1117] border border-[#D29922]/40 p-3 rounded-lg text-xs">
                  <div className="font-bold text-[#D29922]">{ev.service}</div>
                  <div className="text-[#C9D1D9] mt-1">{ev.description}</div>
                </div>
              ))
            ) : (
              <div className="bg-[#0D1117] border border-[#30363D] rounded-lg p-6 text-center text-xs font-mono text-[#3FB950]">
                ✓ All AWS regional services operating normally (No active incidents)
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
