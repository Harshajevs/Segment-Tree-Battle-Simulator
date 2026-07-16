import { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { AttackResult, ChallengeResult } from '../api/types'
import ActionLog from '../components/ActionLog'
import ScoreBoard from '../components/ScoreBoard'
import TeamPanel from '../components/TeamPanel'
import { useMatchStore } from '../store/matchStore'

export default function ArenaPage() {
  const { id } = useParams<{ id: string }>()
  const {
    match,
    soldiers,
    gridOffsets,
    log,
    lastAction,
    loading,
    acting,
    error,
    attackRange,
    defenseRange,
    loadMatch,
    setGridOffset,
    setAttackRange,
    setDefenseRange,
    act,
    clearError,
  } = useMatchStore()

  useEffect(() => {
    if (id) void loadMatch(id)
  }, [id, loadMatch])

  if (loading) return <div className="p-10 text-center text-slate-400">Rebuilding segment trees…</div>
  if (!match) {
    return (
      <div className="p-10 text-center text-slate-400">
        {error ?? 'Match not found.'} <Link to="/" className="text-sky-400 underline">Go home</Link>
      </div>
    )
  }

  const attacker = match.state.attacker
  const isChallenge = match.state.expected_action === 'challenge'
  const finished = match.state.status === 'finished'

  const attackResult = lastAction?.type === 'attack' ? (lastAction.result as AttackResult) : null
  const challengeResult = lastAction?.type === 'challenge' ? (lastAction.result as ChallengeResult) : null

  const panels = [0, 1].map((teamIndex) => {
    const isAttackerPanel = teamIndex === attacker
    return (
      <TeamPanel
        key={teamIndex}
        team={match.teams[teamIndex]}
        soldiers={soldiers[teamIndex]}
        offset={gridOffsets[teamIndex]}
        range={isAttackerPanel ? attackRange : defenseRange}
        rangeLabel={isAttackerPanel ? (isChallenge ? 'GCD/LCM range' : 'Attack range') : 'Defense range'}
        rangeColor={isAttackerPanel ? 'ring-sky-400' : 'ring-rose-400'}
        highlightIndex={
          attackResult
            ? teamIndex === attackResult.attacker
              ? attackResult.champion_index
              : attackResult.target_index
            : undefined
        }
        onRangeChange={isAttackerPanel ? setAttackRange : setDefenseRange}
        onPageChange={(offset) => void setGridOffset(teamIndex as 0 | 1, offset)}
      />
    )
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Link to="/" className="text-sm text-slate-400 hover:text-slate-200">← New battle</Link>
        <Link
          to={`/match/${match.id}/visualizer`}
          className="rounded-lg border border-arena-border bg-arena-panel px-3 py-1.5 text-sm hover:border-sky-700"
        >
          🌳 Tree visualizer
        </Link>
      </div>

      <ScoreBoard match={match} />

      {error && (
        <div className="flex items-center justify-between rounded-lg bg-red-500/10 px-4 py-2 text-sm text-red-300">
          <span>{error}</span>
          <button onClick={clearError} className="text-red-200 underline">dismiss</button>
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-2">{panels}</div>

      {!finished && (
        <div className="rounded-xl border border-arena-border bg-arena-panel p-4 text-center">
          <button
            onClick={() => void act()}
            disabled={acting}
            className={`rounded-lg px-8 py-3 font-semibold text-white transition disabled:opacity-50 ${
              isChallenge ? 'bg-purple-600 hover:bg-purple-500' : 'bg-sky-600 hover:bg-sky-500'
            }`}
          >
            {acting ? 'Resolving…' : isChallenge ? '✨ Resolve GCD/LCM challenge' : `⚔️ ${match.teams[attacker].name} attacks`}
          </button>
          <p className="mt-2 text-xs text-slate-500">
            {isChallenge
              ? 'GCD and LCM of the selected ranges are compared; each duel is worth +50 points.'
              : 'damage = attackSum(attacker range) − healthSum(defender range); lands on the weakest defender.'}
          </p>
        </div>
      )}

      {challengeResult && (
        <div className="rounded-xl border border-purple-800/50 bg-purple-950/30 p-4 text-sm">
          <h3 className="mb-1 font-semibold text-purple-300">Challenge result — round {challengeResult.round}</h3>
          <p>
            GCD {String(challengeResult.gcd_attacker)} vs {String(challengeResult.gcd_defender)} · LCM{' '}
            {String(challengeResult.lcm_attacker)} vs {String(challengeResult.lcm_defender)}
          </p>
        </div>
      )}

      <ActionLog entries={log} />
    </div>
  )
}
