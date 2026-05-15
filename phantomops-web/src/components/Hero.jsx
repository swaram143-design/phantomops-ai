export default function Hero() {
  return (
    <section className="relative overflow-hidden px-8 py-32 text-center">
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-purple-500/10" />

      <div className="relative z-10 max-w-6xl mx-auto">

        <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 text-cyan-300 text-sm mb-8">
          AI AUTOMATION OPERATING SYSTEM
        </div>

        <h1 className="text-7xl md:text-8xl font-black leading-tight tracking-tight">
          Build Your
          <span className="text-cyan-400"> Autonomous </span>
          Business Infrastructure
        </h1>

        <p className="text-zinc-400 text-xl max-w-3xl mx-auto mt-10 leading-relaxed">
          PhantomOps AI helps businesses automate revenue pipelines,
          lead generation, CRM operations, outreach, and intelligent workflows
          using production-grade AI systems.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-5 mt-14">

          <button className="px-10 py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-lg transition">
            Launch Automation
          </button>

          <button className="px-10 py-5 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 text-white font-bold text-lg transition">
            View CRM
          </button>

        </div>

        <div className="grid md:grid-cols-3 gap-6 mt-24">

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl">
            <p className="text-zinc-400 text-sm">AI Runtime</p>
            <h3 className="text-5xl font-black mt-4 text-green-400">
              LIVE
            </h3>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl">
            <p className="text-zinc-400 text-sm">Automation Engine</p>
            <h3 className="text-5xl font-black mt-4 text-cyan-400">
              ACTIVE
            </h3>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl">
            <p className="text-zinc-400 text-sm">AI Agents</p>
            <h3 className="text-5xl font-black mt-4 text-purple-400">
              READY
            </h3>
          </div>

        </div>

      </div>
    </section>
  );
}
