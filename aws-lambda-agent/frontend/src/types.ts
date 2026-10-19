export interface DiagnosticStep {
  step: number;
  tool_selected: string;
  confidence: number;
  probabilities: Record<string, number>;
  tool_result: Record<string, unknown>;
  reasoning: string;
}

export interface Evidence {
  logs?: Record<string, unknown>;
  metrics?: Record<string, unknown>;
  config?: Record<string, unknown>;
  health?: Record<string, unknown>;
}

export interface DiagnoseResponse {
  query: string;
  function_name: string;
  scenario_detected: string;
  decision_trace: DiagnosticStep[];
  evidence: Evidence;
  root_cause: string;
  explanation: string;
  fix_recommendation: string;
  fix_commands: string[];
  synthesis_mode: 'bedrock' | 'demo';
  decider_mode: 'strands-decider-2b' | 'fallback';
}

export interface ApiInfo {
  decider_mode: 'strands-decider-2b' | 'fallback';
  synthesis_mode: 'bedrock' | 'demo';
  version?: string;
  status?: string;
}
