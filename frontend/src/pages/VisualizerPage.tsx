import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, ApiError } from '../api/client'
import type { Attribute, Match, OperationName, QueryOut, TreeOut } from '../api/types'
import TreeView from '../components/TreeView'

const OPERATIONS: { value: OperationName; label: string }[] = [
  { value: 'sum', label: 'Range sum' },
  { value: 'max', label: 'Max index' },
  { value: 'min', label: 'Min index' },
  { value: 'gcd', label: 'Range GCD' },
  { value: 'lcm', label: 'Range LCM' },
]

export default function VisualizerPage() {
  const { id } = useParams<{ id: string }>()
  const [match, setMatch] = useState<Match | null>(null)
  const [team, setTeam] = useState<0 | 1>(0)
  const [attribute, setAttribute] = useState<Attribute>('attack')
  const [operation, setOperation] = useState<OperationName>('sum')
  const [depth, setDepth] = useState(4)
  const [tree, setTree] = useState<TreeOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const [queryLeft, setQueryLeft] = useState(0)
  const [queryRight, setQueryRight] = useState(7)
  const [queryResult, setQueryResult] = useState<QueryOut | null>(null)
  const [querying, setQuerying] = useState(false)

  const loadTree = useCallback(async () => {
    if (!id) return
    setError(null)
    try {
      const [freshMatch, freshTree] = await Promise.all([
        api.getMatch(id),
        api.tree(id, team, attribute, operation, depth),
      ])
      setMatch(freshMatch)
      setTree(freshTree)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to load tree')
    }
  }, [id, team, attribute, operation, depth])

  useEffect(() => {
    void loadTree()
  }, [loadTree])

  const runQuery = async () => {
    if (!id) return
    setQuerying(true)
    setError(null)
    try {
      setQueryResult(await api.query(id, team, attribute, operation, queryLeft, queryRight))
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Query failed')
      setQueryResult(null)
    } finally {
      setQuerying(false)
    }
  }

  const select = 'rounded border border-arena-border bg-arena-bg px-2 py-1.5 text-sm'

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Link to={`/match/${id}`} className="text-sm text-slate-400 hover:text-slate-200">← Back to arena</Link>
        {match && (
          <span className="text-sm text-slate-400">
            {match.team_size.toLocaleString()} soldiers · round {match.state.round}
          </span>
        )}
      </div>

      <div className="rounded-xl border border-arena-border bg-arena-panel p-4">
        <h2 className="mb-3 font-semibold">🌳 Segment tree visualizer</h2>
        <div className="flex flex-wrap items-end gap-3 text-sm">
          <label>
            <span className="mb-1 block text-xs text-slate-400">Team</span>
            <select value={team} onChange={(e) => setTeam(Number(e.target.value) as 0 | 1)} className={select}>
              <option value={0}>Team A</option>
              <option value={1}>Team B</option>
            </select>
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Attribute</span>
            <select value={attribute} onChange={(e) => setAttribute(e.target.value as Attribute)} className={select}>
              <option value="attack">Attack</option>
              <option value="health">Health</option>
            </select>
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Operation</span>
            <select value={operation} onChange={(e) => setOperation(e.target.value as OperationName)} className={select}>
              {OPERATIONS.map((op) => (
                <option key={op.value} value={op.value}>{op.label}</option>
              ))}
            </select>
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Depth: {depth}</span>
            <input
              type="range"
              min={1}
              max={8}
              value={depth}
              onChange={(e) => setDepth(Number(e.target.value))}
              className="w-32"
            />
          </label>
          <button
            onClick={() => void loadTree()}
            className="rounded-lg border border-arena-border px-3 py-1.5 hover:border-sky-700"
          >
            ↻ Refresh
          </button>
        </div>
        <p className="mt-2 text-xs text-slate-500">
          {operation === 'max' || operation === 'min'
            ? 'Index trees store the position of the winning soldier, not the value — hover soldiers in the arena to cross-reference.'
            : 'Internal nodes hold the operation applied over their [start, end] range; leaves are individual soldiers.'}
        </p>
      </div>

      {error && <div className="rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-300">{error}</div>}

      {tree && <TreeView tree={tree} />}

      <div className="rounded-xl border border-arena-border bg-arena-panel p-4">
        <h2 className="mb-3 font-semibold">🔎 Query playground</h2>
        <div className="flex flex-wrap items-end gap-3 text-sm">
          <label>
            <span className="mb-1 block text-xs text-slate-400">Left</span>
            <input
              type="number"
              min={0}
              value={queryLeft}
              onChange={(e) => setQueryLeft(Number(e.target.value))}
              className={`${select} w-28`}
            />
          </label>
          <label>
            <span className="mb-1 block text-xs text-slate-400">Right</span>
            <input
              type="number"
              min={0}
              value={queryRight}
              onChange={(e) => setQueryRight(Number(e.target.value))}
              className={`${select} w-28`}
            />
          </label>
          <button
            onClick={() => void runQuery()}
            disabled={querying}
            className="rounded-lg bg-sky-600 px-4 py-1.5 font-semibold text-white hover:bg-sky-500 disabled:opacity-50"
          >
            {querying ? 'Querying…' : 'Run O(log n) query'}
          </button>
        </div>
        {queryResult && (
          <div className="mt-3 rounded-lg bg-arena-bg/60 p-3 text-sm">
            <span className="text-slate-400">
              {queryResult.operation}({queryResult.attribute}[{queryResult.left}..{queryResult.right}]) ={' '}
            </span>
            <span className="font-mono text-lg font-bold text-sky-300">{String(queryResult.value)}</span>
            {queryResult.element_value !== null && (
              <span className="ml-2 text-slate-400">
                (soldier #{String(queryResult.value)} has {queryResult.attribute} {queryResult.element_value})
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
