import type {
  ActionLogItem,
  ActionOut,
  ActionRequest,
  Attribute,
  Match,
  MatchCreate,
  MatchListItem,
  OperationName,
  QueryOut,
  SoldiersOut,
  TreeOut,
} from './types'

// Same-origin by default (Vite dev proxy / combined deploy); set VITE_API_URL
// at build time when the API lives on another host.
const BASE_URL = import.meta.env.VITE_API_URL ?? ''

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`
    try {
      const body = await response.json()
      message = body?.error?.message ?? body?.detail?.[0]?.msg ?? message
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(response.status, message)
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<{ status: string; ai_provider: string }>('/api/health'),

  createMatch: (payload: MatchCreate) =>
    request<Match>('/api/matches', { method: 'POST', body: JSON.stringify(payload) }),

  listMatches: () => request<MatchListItem[]>('/api/matches'),

  getMatch: (id: string) => request<Match>(`/api/matches/${id}`),

  act: (id: string, action: ActionRequest) =>
    request<ActionOut>(`/api/matches/${id}/actions`, {
      method: 'POST',
      body: JSON.stringify(action),
    }),

  actionLog: (id: string) => request<ActionLogItem[]>(`/api/matches/${id}/actions`),

  query: (id: string, team: number, attribute: Attribute, operation: OperationName, left: number, right: number) =>
    request<QueryOut>(
      `/api/matches/${id}/query?team=${team}&attribute=${attribute}&operation=${operation}&left=${left}&right=${right}`,
    ),

  tree: (id: string, team: number, attribute: Attribute, operation: OperationName, maxDepth = 5) =>
    request<TreeOut>(
      `/api/matches/${id}/tree?team=${team}&attribute=${attribute}&operation=${operation}&max_depth=${maxDepth}`,
    ),

  soldiers: (id: string, team: number, offset = 0, limit = 256) =>
    request<SoldiersOut>(`/api/matches/${id}/soldiers?team=${team}&offset=${offset}&limit=${limit}`),
}
