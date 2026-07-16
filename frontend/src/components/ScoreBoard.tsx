import type { Match } from '../api/types'

const TEAM_COLORS = ['text-team-a', 'text-team-b']

export default function ScoreBoard({ match }: { match: Match }) {
  const { state, teams } = match
  const finished = state.status === 'finished'
  return (
    <div className="rounded-xl border border-arena-border bg-arena-panel p-4">
      <div className="flex items-center justify-between gap-4">
        {teams.map((team, i) => (
          <div key={team.index} className={`flex-1 ${i === 1 ? 'text-right' : ''}`}>
            <div className={`text-sm font-semibold ${TEAM_COLORS[i]}`}>
              {team.name}
              {!finished && state.attacker === i && (
                <span className="ml-2 rounded bg-amber-500/20 px-1.5 py-0.5 text-xs text-amber-300">attacking</span>
              )}
            </div>
            <div className="text-3xl font-bold tabular-nums">{state.scores[i].toLocaleString()}</div>
            <div className="text-xs text-slate-400">
              ⚔ {team.total_attack.toLocaleString()} · ❤ {team.total_health.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
      <div className="mt-3 text-center text-sm">
        {finished ? (
          <span className="rounded-lg bg-emerald-500/15 px-3 py-1 font-semibold text-emerald-300">
            {state.winner === null ? "It's a tie!" : `${teams[state.winner].name} wins!`}
          </span>
        ) : (
          <span className="text-slate-400">
            Round <span className="font-semibold text-slate-200">{state.round}</span> / {match.max_rounds}
            {state.expected_action === 'challenge' && (
              <span className="ml-2 rounded bg-purple-500/20 px-2 py-0.5 text-xs font-semibold text-purple-300">
                ✨ GCD/LCM challenge round
              </span>
            )}
          </span>
        )}
      </div>
    </div>
  )
}
