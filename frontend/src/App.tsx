import { Suspense, lazy } from 'react'
import { Link, Route, Routes } from 'react-router-dom'

const HomePage = lazy(() => import('./pages/HomePage'))
const ArenaPage = lazy(() => import('./pages/ArenaPage'))
const VisualizerPage = lazy(() => import('./pages/VisualizerPage'))

function Fallback() {
  return <div className="p-10 text-center text-slate-400">Loading…</div>
}

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-arena-border bg-arena-panel/70 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link to="/" className="text-lg font-bold tracking-tight">
            ⚔️ Segment Tree <span className="text-team-a">Battle</span> Simulator
          </Link>
          <a
            href="https://github.com/Harshajevs/Segment-Tree-Battle-Simulator"
            target="_blank"
            rel="noreferrer"
            className="text-sm text-slate-400 hover:text-slate-200"
          >
            GitHub
          </a>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6">
        <Suspense fallback={<Fallback />}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/match/:id" element={<ArenaPage />} />
            <Route path="/match/:id/visualizer" element={<VisualizerPage />} />
            <Route path="*" element={<Fallback />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  )
}
