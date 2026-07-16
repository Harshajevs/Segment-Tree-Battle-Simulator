import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, ApiError } from '../api/client'
import type { MatchListItem } from '../api/types'

const FIELDS = [
  { key: 'team_size', label: 'Soldiers per team', min: 8, max: 100000 },
  { key: 'seed', label: 'Random seed', min: 0, max: 2147483647 },
  { key: 'max_rounds', label: 'Max rounds', min: 1, max: 1000 },
  { key: 'challenge_interval', label: 'Challenge every N rounds', min: 2, max: 100 },
] as const

type FormState = { team_size: number; seed: number; max_rounds: number; challenge_interval: number }

export default function HomePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState<FormState>({ team_size: 32, seed: 42, max_rounds: 20, challenge_interval: 10 })
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [recent, setRecent] = useState<MatchListItem[]>([])

  useEffect(() => {
    api.listMatches().then(setRecent).catch(() => setRecent([]))
  }, [])

  const createMatch = async () => {
    setCreating(true)
    setError(null)
    try {
      const match = await api.createMatch(form)
      navigate(`/match/${match.id}`)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not reach the backend — is it running on port 8000?')
      setCreating(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <section className="mb-8 text-center">
        <h1 className="mb-2 text-3xl font-bold">Turn-based battles, powered by segment trees</h1>
        <p className="text-slate-400">
          Every attack is a range-sum query. Every target is a min-index query. Every challenge round is a GCD/LCM
          duel. All in O(log n) — watch the tree update live.
        </p>
      </section>

      <section className="rounded-xl border border-arena-border bg-arena-panel p-6">
        <h2 className="mb-4 text-lg font-semibold">New battle</h2>
        <div className="grid grid-cols-2 gap-4">
          {FIELDS.map((field) => (
            <label key={field.key} className="text-sm">
              <span className="mb-1 block text-slate-400">{field.label}</span>
              <input
                type="number"
                min={field.min}
                max={field.max}
                value={form[field.key]}
                onChange={(event) => setForm({ ...form, [field.key]: Number(event.target.value) })}
                className="w-full rounded border border-arena-border bg-arena-bg px-3 py-2"
              />
            </label>
          ))}
        </div>
        {error && <p className="mt-3 rounded bg-red-500/10 px-3 py-2 text-sm text-red-300">{error}</p>}
        <button
          onClick={createMatch}
          disabled={creating}
          className="mt-4 w-full rounded-lg bg-sky-600 py-2.5 font-semibold text-white transition hover:bg-sky-500 disabled:opacity-50"
        >
          {creating ? 'Building segment trees…' : '⚔️ Start battle'}
        </button>
        <p className="mt-2 text-center text-xs text-slate-500">
          Same seed → identical armies. Tip: 32–64 soldiers is ideal for the visualizer; up to 100,000 supported.
        </p>
      </section>

      {recent.length > 0 && (
        <section className="mt-8">
          <h2 className="mb-3 text-lg font-semibold">Recent matches</h2>
          <ul className="space-y-2">
            {recent.map((match) => (
              <li key={match.id}>
                <Link
                  to={`/match/${match.id}`}
                  className="flex items-center justify-between rounded-lg border border-arena-border bg-arena-panel px-4 py-2.5 text-sm transition hover:border-sky-700"
                >
                  <span className="font-mono text-xs text-slate-400">{match.id.slice(0, 8)}</span>
                  <span>
                    {match.team_size.toLocaleString()} soldiers · round {match.round}/{match.max_rounds}
                  </span>
                  <span className="tabular-nums">
                    {match.scores[0].toLocaleString()} : {match.scores[1].toLocaleString()}
                  </span>
                  <span
                    className={
                      match.status === 'finished' ? 'text-emerald-400' : 'text-amber-300'
                    }
                  >
                    {match.status === 'finished'
                      ? match.winner === null
                        ? 'tie'
                        : `Team ${'AB'[match.winner]} won`
                      : 'in progress'}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
