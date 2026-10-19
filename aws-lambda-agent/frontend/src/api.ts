import axios from 'axios';
import type { DiagnoseResponse, ApiInfo } from './types';

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function diagnose(query: string, functionName: string): Promise<DiagnoseResponse> {
  const response = await client.post<DiagnoseResponse>('/api/diagnose', {
    query,
    function_name: functionName || undefined,
  });
  return response.data;
}

export async function getApiInfo(): Promise<ApiInfo> {
  const response = await client.get<ApiInfo>('/api/info');
  return response.data;
}
