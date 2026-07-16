import type { LogEntry } from '../store/matchStore'
import type { AttackResult, ChallengeResult } from '../api/types'

const TEAM_NAMES = ['Team A', 'Team B']

function summary(entry: LogEntry): string {
  if (entry.type === 'attack') {
    const r = entry.result as AttackResult
    return `${TEAM_NAMES[r.attacker]} hit soldier #${r.target_index} for ${r.damage.toLocaleString()} (${r.attack_sum.toLocaleString()} atk vs ${r.defense_sum.toLocaleString()} def)`
  }
  const r = entry.result as ChallengeResult
  const name = (winner: 0 | 1 | null) => (winner === null ? 'tie' : TEAM_NAMES[winner])
  return `Challenge — GCD: ${name(r.gcd_winner)} (${r.gcd_attacker} vs ${r.gcd_defender}), LCM: ${name(r.lcm_winner)}`
}

export default function ActionLog({ entries }: { entries: LogEntry[] }) {
  return (
    <div className="rounded-xl border border-arena-border bg-arena-panel p-4">
      <h3 className="mb-3 font-semibold">Battle log</h3>
      {entries.length === 0 ? (
        <p className="text-sm text-slate-400">No actions yet — pick your ranges and attack.</p>
      ) : (
        <ol className="max-h-80 space-y-2 overflow-y-auto pr-1 text-sm">
          {[...entries].reverse().map((entry) => (
            <li key={entry.sequence} className="rounded-lg bg-arena-bg/60 p-2">
              <div className="flex items-start gap-2">
                <span className="mt-0.5 shrink-0 rounded bg-arena-border px-1.5 text-xs tabular-nums text-slate-300">
                  R{entry.result.round}
                </span>
                <div>
                  <div className="text-slate-200">{summary(entry)}</div>
                  {entry.commentary && (
                    <div className="mt-1 text-xs italic text-sky-300/80">🎙 {entry.commentary}</div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
