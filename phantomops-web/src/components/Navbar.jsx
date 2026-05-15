export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/60 backdrop-blur-xl border-b border-cyan-500/10">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black tracking-wide text-cyan-400">
            PhantomOps AI
          </h1>

          <p className="text-zinc-500 text-sm">
            Autonomous Revenue Infrastructure
          </p>
        </div>

        <div className="flex items-center gap-4">
          <button className="px-5 py-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition">
            Open CRM
          </button>

          <button className="px-5 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-black transition">
            Start Automation
          </button>
        </div>
      </div>
    </nav>
  );
}
