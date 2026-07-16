import { useMemo } from 'react'
import type { TreeNode, TreeOut } from '../api/types'

interface TreeViewProps {
  tree: TreeOut
  highlightNodes?: Set<number>
}

const NODE_RADIUS = 26
const LEVEL_HEIGHT = 88
const MIN_GAP = 64

function label(payload: TreeNode['payload']): string {
  const text = String(payload)
  return text.length > 7 ? `${text.slice(0, 6)}…` : text
}

export default function TreeView({ tree, highlightNodes }: TreeViewProps) {
  const { nodes } = tree

  const layout = useMemo(() => {
    const maxDepth = Math.max(...nodes.map((n) => n.depth))
    const leaves = Math.min(2 ** maxDepth, nodes.filter((n) => n.depth === maxDepth).length)
    const width = Math.max(720, leaves * MIN_GAP)
    const height = (maxDepth + 1) * LEVEL_HEIGHT + NODE_RADIUS
    // x position: centre of the node's covered range, scaled to the full span
    const span = nodes[0].end - nodes[0].start || 1
    const positions = new Map<number, { x: number; y: number }>()
    for (const node of nodes) {
      const centre = (node.start + node.end) / 2 - nodes[0].start
      positions.set(node.node, {
        x: NODE_RADIUS + 10 + (centre / span) * (width - 2 * (NODE_RADIUS + 10)),
        y: NODE_RADIUS + 8 + node.depth * LEVEL_HEIGHT,
      })
    }
    return { width, height, positions }
  }, [nodes])

  const byId = useMemo(() => new Map(nodes.map((n) => [n.node, n])), [nodes])

  return (
    <div className="overflow-x-auto rounded-xl border border-arena-border bg-arena-panel p-2">
      <svg width={layout.width} height={layout.height} className="mx-auto block">
        {nodes.map((node) => {
          const parent = node.node > 1 ? layout.positions.get(Math.floor(node.node / 2)) : null
          const self = layout.positions.get(node.node)!
          return (
            parent && (
              <line
                key={`edge-${node.node}`}
                x1={parent.x}
                y1={parent.y}
                x2={self.x}
                y2={self.y}
                stroke="#26304d"
                strokeWidth={1.5}
              />
            )
          )
        })}
        {nodes.map((node) => {
          const { x, y } = layout.positions.get(node.node)!
          const isLeaf = node.start === node.end
          const truncated = !isLeaf && !byId.has(node.node * 2)
          const highlighted = highlightNodes?.has(node.node)
          return (
            <g key={node.node}>
              <circle
                cx={x}
                cy={y}
                r={NODE_RADIUS}
                fill={highlighted ? '#f59e0b' : isLeaf ? '#0e7490' : '#1e293b'}
                stroke={highlighted ? '#fbbf24' : '#38bdf8'}
                strokeWidth={highlighted ? 3 : 1.5}
              />
              <text x={x} y={y - 2} textAnchor="middle" fill="#e2e8f0" fontSize={11} fontWeight={700}>
                {label(node.payload)}
              </text>
              <text x={x} y={y + 11} textAnchor="middle" fill="#94a3b8" fontSize={9}>
                [{node.start},{node.end}]
              </text>
              {truncated && (
                <text x={x} y={y + NODE_RADIUS + 12} textAnchor="middle" fill="#64748b" fontSize={10}>
                  ⋯
                </text>
              )}
            </g>
          )
        })}
      </svg>
    </div>
  )
}
