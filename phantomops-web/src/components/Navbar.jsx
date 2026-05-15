
export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/70 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-5">
        <div>
          <h1 className="text-3xl font-black text-cyan-400">
            PhantomOps AI
          </h1>

          <p className="text-zinc-500 text-sm">
            Autonomous AI Infrastructure
          </p>
        </div>

        <div className="flex items-center gap-4">
          <button className="px-5 py-3 rounded-xl bg-white/5 border border-white/10">
            Open CRM
          </button>

          <button className="px-5 py-3 rounded-xl bg-cyan-500 text-black font-bold">
            Start Automation
          </button>
        </div>
      </div>
    </nav>
  );
}
