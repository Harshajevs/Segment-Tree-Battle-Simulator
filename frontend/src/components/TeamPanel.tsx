import type { Range, Soldier, TeamSummary } from '../api/types'
import { GRID_LIMIT } from '../store/matchStore'

interface TeamPanelProps {
  team: TeamSummary
  soldiers: Soldier[]
  offset: number
  range: Range
  rangeLabel: string
  rangeColor: string
  highlightIndex?: number
  onRangeChange: (range: Range) => void
  onPageChange: (offset: number) => void
}

function healthColor(health: number): string {
  if (health === 0) return 'bg-slate-700'
  if (health < 400) return 'bg-red-500/70'
  if (health < 800) return 'bg-amber-500/70'
  return 'bg-emerald-500/70'
}

export default function TeamPanel({
  team,
  soldiers,
  offset,
  range,
  rangeLabel,
  rangeColor,
  highlightIndex,
  onRangeChange,
  onPageChange,
}: TeamPanelProps) {
  const clamp = (value: number) => Math.max(0, Math.min(team.size - 1, value))

  const setLeft = (left: number) =>
    onRangeChange({ left: clamp(left), right: Math.max(clamp(left), range.right) })
  const setRight = (right: number) =>
    onRangeChange({ left: Math.min(range.left, clamp(right)), right: clamp(right) })

  const handleCellClick = (index: number) => {
    // first click anchors the range, second click extends it
    if (index < range.left || range.left !== range.right) onRangeChange({ left: index, right: index })
    else onRangeChange({ left: range.left, right: index })
  }

  const pages = Math.ceil(team.size / GRID_LIMIT)
  const page = Math.floor(offset / GRID_LIMIT)

  return (
    <div className="rounded-xl border border-arena-border bg-arena-panel p-4">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-semibold">{team.name}</h3>
        <span className="text-xs text-slate-400">{team.size.toLocaleString()} soldiers</span>
      </div>

      <div className="mb-3 grid grid-cols-[repeat(16,minmax(0,1fr))] gap-0.5">
        {soldiers.map((soldier) => {
          const selected = soldier.index >= range.left && soldier.index <= range.right
          const highlighted = soldier.index === highlightIndex
          return (
            <button
              key={soldier.index}
              onClick={() => handleCellClick(soldier.index)}
              title={`#${soldier.index} — attack ${soldier.attack}, health ${soldier.health}`}
              className={`aspect-square rounded-sm transition-transform hover:scale-125 ${healthColor(soldier.health)} ${
                selected ? `ring-2 ${rangeColor}` : ''
              } ${highlighted ? 'animate-pulse ring-2 ring-white' : ''}`}
            />
          )
        })}
      </div>

      {pages > 1 && (
        <div className="mb-3 flex items-center justify-between text-xs text-slate-400">
          <button
            disabled={page === 0}
            onClick={() => onPageChange((page - 1) * GRID_LIMIT)}
            className="rounded border border-arena-border px-2 py-1 disabled:opacity-40"
          >
            ← prev
          </button>
          <span>
            showing {offset}–{Math.min(offset + GRID_LIMIT, team.size) - 1} · page {page + 1}/{pages}
          </span>
          <button
            disabled={page >= pages - 1}
            onClick={() => onPageChange((page + 1) * GRID_LIMIT)}
            className="rounded border border-arena-border px-2 py-1 disabled:opacity-40"
          >
            next →
          </button>
        </div>
      )}

      <div className="flex items-center gap-2 text-sm">
        <span className="w-24 shrink-0 text-xs text-slate-400">{rangeLabel}</span>
        <input
          type="number"
          min={0}
          max={team.size - 1}
          value={range.left}
          onChange={(event) => setLeft(Number(event.target.value))}
          className="w-24 rounded border border-arena-border bg-arena-bg px-2 py-1"
          aria-label={`${rangeLabel} start`}
        />
        <span className="text-slate-500">to</span>
        <input
          type="number"
          min={0}
          max={team.size - 1}
          value={range.right}
          onChange={(event) => setRight(Number(event.target.value))}
          className="w-24 rounded border border-arena-border bg-arena-bg px-2 py-1"
          aria-label={`${rangeLabel} end`}
        />
      </div>
    </div>
  )
}
