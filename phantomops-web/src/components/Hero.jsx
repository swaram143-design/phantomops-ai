export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.18),transparent_45%)]" />

      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[900px] bg-cyan-500/10 blur-[180px] rounded-full" />

      <div className="relative z-10 max-w-7xl mx-auto text-center pt-36">

        <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full border border-green-500/20 bg-green-500/5 text-green-400 uppercase tracking-[0.25em] text-xs mb-10">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          AI Runtime Online
        </div>

        <h1 className="text-6xl md:text-8xl font-black leading-none tracking-tight">
          Autonomous
          <span className="block text-cyan-400">
            Business Operations
          </span>
        </h1>

        <p className="text-zinc-400 text-xl leading-relaxed max-w-3xl mx-auto mt-10">
          PhantomOps AI deploys intelligent automation systems for
          lead generation, CRM workflows, healthcare automation,
          outreach systems, analytics, and autonomous commercial operations.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-5 mt-14">

          <button className="px-10 py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-lg transition">
            Deploy AI Infrastructure
          </button>

          <button className="px-10 py-5 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 font-bold text-lg transition">
            View Capabilities
          </button>

        </div>

      </div>
    </section>
  );
}
