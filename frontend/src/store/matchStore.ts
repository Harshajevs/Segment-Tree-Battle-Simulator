import { create } from 'zustand'
import { api, ApiError } from '../api/client'
import type { ActionOut, ActionType, Match, Range, Soldier } from '../api/types'

export interface LogEntry {
  sequence: number
  type: ActionType
  result: ActionOut['result']
  commentary: string | null
}

// soldier grids are capped client-side; larger teams paginate via offsets
export const GRID_LIMIT = 256

interface MatchStore {
  match: Match | null
  soldiers: [Soldier[], Soldier[]]
  gridOffsets: [number, number]
  log: LogEntry[]
  lastAction: ActionOut | null
  loading: boolean
  acting: boolean
  error: string | null
  attackRange: Range
  defenseRange: Range

  loadMatch: (id: string) => Promise<void>
  setGridOffset: (team: 0 | 1, offset: number) => Promise<void>
  setAttackRange: (range: Range) => void
  setDefenseRange: (range: Range) => void
  act: () => Promise<void>
  clearError: () => void
}

function message(error: unknown): string {
  if (error instanceof ApiError) return error.message
  if (error instanceof Error) return error.message
  return 'Unexpected error'
}

export const useMatchStore = create<MatchStore>((set, get) => ({
  match: null,
  soldiers: [[], []],
  gridOffsets: [0, 0],
  log: [],
  lastAction: null,
  loading: false,
  acting: false,
  error: null,
  attackRange: { left: 0, right: 0 },
  defenseRange: { left: 0, right: 0 },

  loadMatch: async (id) => {
    set({ loading: true, error: null, lastAction: null })
    try {
      const [match, teamA, teamB, actions] = await Promise.all([
        api.getMatch(id),
        api.soldiers(id, 0, 0, GRID_LIMIT),
        api.soldiers(id, 1, 0, GRID_LIMIT),
        api.actionLog(id),
      ])
      const right = Math.min(7, match.team_size - 1)
      set({
        match,
        soldiers: [teamA.soldiers, teamB.soldiers],
        gridOffsets: [0, 0],
        log: actions.map(({ sequence, type, result, commentary }) => ({ sequence, type, result, commentary })),
        attackRange: { left: 0, right },
        defenseRange: { left: 0, right },
        loading: false,
      })
    } catch (error) {
      set({ error: message(error), loading: false })
    }
  },

  setGridOffset: async (team, offset) => {
    const { match, soldiers, gridOffsets } = get()
    if (!match) return
    try {
      const page = await api.soldiers(match.id, team, offset, GRID_LIMIT)
      const nextSoldiers: [Soldier[], Soldier[]] = [...soldiers]
      const nextOffsets: [number, number] = [...gridOffsets]
      nextSoldiers[team] = page.soldiers
      nextOffsets[team] = offset
      set({ soldiers: nextSoldiers, gridOffsets: nextOffsets })
    } catch (error) {
      set({ error: message(error) })
    }
  },

  setAttackRange: (attackRange) => set({ attackRange }),
  setDefenseRange: (defenseRange) => set({ defenseRange }),

  act: async () => {
    const { match, attackRange, defenseRange, log } = get()
    if (!match || match.state.expected_action === 'none') return
    set({ acting: true, error: null })
    try {
      const action = await api.act(match.id, {
        type: match.state.expected_action as ActionType,
        attack_range: attackRange,
        defense_range: defenseRange,
      })
      // refresh authoritative state + affected soldier pages
      const [fresh, teamA, teamB] = await Promise.all([
        api.getMatch(match.id),
        api.soldiers(match.id, 0, get().gridOffsets[0], GRID_LIMIT),
        api.soldiers(match.id, 1, get().gridOffsets[1], GRID_LIMIT),
      ])
      set({
        match: fresh,
        soldiers: [teamA.soldiers, teamB.soldiers],
        log: [...log, { sequence: action.sequence, type: action.type, result: action.result, commentary: action.commentary }],
        lastAction: action,
        acting: false,
      })
    } catch (error) {
      set({ error: message(error), acting: false })
    }
  },

  clearError: () => set({ error: null }),
}))
