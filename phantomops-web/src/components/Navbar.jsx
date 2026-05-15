export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-8 py-6 border-b border-white/10 bg-black/80 backdrop-blur-xl sticky top-0 z-50">
      <div>
        <h1 className="text-3xl font-black tracking-wide text-cyan-400">
          PhantomOps AI
        </h1>

        <p className="text-zinc-400 text-sm">
          Revenue Automation Infrastructure
        </p>
      </div>

      <div className="flex items-center gap-4">
        <button className="px-5 py-2 rounded-full bg-purple-500 hover:bg-purple-400 text-white font-semibold transition">
          Open CRM
        </button>

        <button className="px-5 py-2 rounded-full bg-cyan-500 hover:bg-cyan-400 text-black font-semibold transition">
          Start Automation
        </button>
      </div>
    </nav>
  );
}
