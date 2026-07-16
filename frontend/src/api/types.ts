// Mirrors backend/app/schemas/match.py. Values that can exceed
// Number.MAX_SAFE_INTEGER (range LCMs) arrive as decimal strings.
export type Attribute = 'attack' | 'health'
export type OperationName = 'sum' | 'max' | 'min' | 'gcd' | 'lcm'
export type ActionType = 'attack' | 'challenge'
export type BigValue = number | string

export interface MatchState {
  round: number
  scores: [number, number]
  attacker: 0 | 1
  status: 'in_progress' | 'finished'
  winner: 0 | 1 | null
  expected_action: 'attack' | 'challenge' | 'none'
}

export interface TeamSummary {
  index: number
  name: string
  size: number
  total_health: number
  total_attack: number
}

export interface Match {
  id: string
  created_at: string
  team_size: number
  seed: number
  max_rounds: number
  challenge_interval: number
  state: MatchState
  teams: TeamSummary[]
}

export interface MatchListItem {
  id: string
  created_at: string
  team_size: number
  max_rounds: number
  status: string
  winner: 0 | 1 | null
  round: number
  scores: [number, number]
}

export interface MatchCreate {
  team_size: number
  seed: number
  max_rounds: number
  challenge_interval: number
}

export interface Range {
  left: number
  right: number
}

export interface ActionRequest {
  type: ActionType
  attack_range: Range
  defense_range: Range
}

export interface AttackResult {
  type: 'attack'
  round: number
  attacker: 0 | 1
  attack_range: [number, number]
  defense_range: [number, number]
  attack_sum: number
  defense_sum: number
  damage: number
  target_index: number
  target_health_before: number
  target_health_after: number
  champion_index: number
  champion_attack_before: number
  champion_attack_after: number
  update_paths?: Record<string, Record<OperationName, number[]>>
}

export interface ChallengeResult {
  type: 'challenge'
  round: number
  attacker: 0 | 1
  attack_range: [number, number]
  defense_range: [number, number]
  gcd_attacker: BigValue
  gcd_defender: BigValue
  gcd_winner: 0 | 1 | null
  lcm_attacker: BigValue
  lcm_defender: BigValue
  lcm_winner: 0 | 1 | null
  bonus: number
}

export type ActionResult = AttackResult | ChallengeResult

export interface ActionOut {
  sequence: number
  type: ActionType
  result: ActionResult
  commentary: string | null
  state: MatchState
}

export interface ActionLogItem {
  sequence: number
  type: ActionType
  result: ActionResult
  commentary: string | null
  created_at: string
}

export interface QueryOut {
  team: number
  attribute: Attribute
  operation: OperationName
  left: number
  right: number
  value: BigValue
  element_value: number | null
}

export interface TreeNode {
  node: number
  start: number
  end: number
  depth: number
  payload: BigValue
}

export interface TreeOut {
  team: number
  attribute: Attribute
  operation: OperationName
  size: number
  max_depth: number
  nodes: TreeNode[]
}

export interface Soldier {
  index: number
  attack: number
  health: number
}

export interface SoldiersOut {
  team: number
  offset: number
  total: number
  soldiers: Soldier[]
}
