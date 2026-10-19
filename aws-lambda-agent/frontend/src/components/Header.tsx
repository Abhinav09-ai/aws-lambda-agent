import React from 'react';

interface HeaderProps {
  deciderMode: string;
  synthesisMode: string;
}

export const Header: React.FC<HeaderProps> = ({ deciderMode, synthesisMode }) => {
  const isRealDecider = deciderMode === 'strands-decider-2b';
  const isBedrock = synthesisMode === 'bedrock';

  return (
    <header className="bg-[#232F3E] border-b border-[#30363D] px-6 py-3 flex items-center justify-between sticky top-0 z-50 shadow-md">
      <div className="flex items-center space-x-3">
        <div className="bg-[#FF9900] text-[#0D1117] font-bold px-2 py-1 rounded text-sm tracking-wider">
          AWS
        </div>
        <h1 className="text-lg font-semibold text-white tracking-wide">
          Lambda Troubleshooting Agent
        </h1>
        <span className="text-xs text-[#8B949E] bg-[#161B22] border border-[#30363D] px-2 py-0.5 rounded-full font-mono">
          #strands-decider-2b #tool-selection
        </span>
      </div>

      <div className="flex items-center space-x-3 text-xs">
        <div className="flex items-center space-x-1.5 bg-[#161B22] border border-[#30363D] px-3 py-1.5 rounded-full">
          <span className={`w-2 h-2 rounded-full ${isRealDecider ? 'bg-[#3FB950] animate-pulse' : 'bg-[#D29922]'}`}></span>
          <span className="text-[#8B949E]">Decider:</span>
          <span className={`font-semibold font-mono ${isRealDecider ? 'text-[#3FB950]' : 'text-[#D29922]'}`}>
            {isRealDecider ? 'Strands Decider 2B' : 'Decider 2B Pattern (Local)'}
          </span>
        </div>

        <div className="flex items-center space-x-1.5 bg-[#161B22] border border-[#30363D] px-3 py-1.5 rounded-full">
          <span className={`w-2 h-2 rounded-full ${isBedrock ? 'bg-[#58A6FF]' : 'bg-[#FF9900]'}`}></span>
          <span className="text-[#8B949E]">Synthesis:</span>
          <span className={`font-semibold font-mono ${isBedrock ? 'text-[#58A6FF]' : 'text-[#FF9900]'}`}>
            {isBedrock ? 'Bedrock (Claude 3)' : 'Verified Demo Mode'}
          </span>
        </div>
      </div>
    </header>
  );
};
