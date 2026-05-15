export default function CTA() {
  return (
    <section className="px-6 py-32 bg-black">
      <div className="max-w-5xl mx-auto bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-white/10 rounded-[40px] p-16 text-center">

        <p className="text-cyan-400 uppercase tracking-[0.25em] text-xs mb-5">
          Launch Infrastructure
        </p>

        <h2 className="text-6xl font-black leading-none">
          Build Your AI Operations Layer
        </h2>

        <p className="text-zinc-400 text-xl leading-relaxed mt-10 max-w-3xl mx-auto">
          Deploy production-grade automation systems that continuously
          optimize workflows, operations, and revenue pipelines.
        </p>

        <div className="flex flex-wrap justify-center gap-5 mt-14">

          <button className="px-10 py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-lg">
            Request Consultation
          </button>

          <button className="px-10 py-5 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 font-bold text-lg">
            Open CRM
          </button>

        </div>

      </div>
    </section>
  );
}
