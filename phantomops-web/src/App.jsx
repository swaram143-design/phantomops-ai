export default function PhantomOpsGodmode() {
  const runtime = [
    ["Marketplace Intelligence", "ACTIVE"],
    ["CRM Analytics", "ACTIVE"],
    ["Proposal Engine", "ARMED"],
    ["Revenue Tracker", "LIVE"],
    ["Inbox Monitoring", "ONLINE"],
    ["WhatsApp Automation", "RUNNING"],
  ];

  const services = [
    {
      icon: "🤖",
      title: "Autonomous AI Operations",
      desc: "Deploy intelligent systems that monitor, analyze, automate, and optimize business workflows continuously.",
    },
    {
      icon: "📈",
      title: "Revenue Intelligence",
      desc: "AI-powered CRM infrastructure, lead pipelines, proposal generation, and predictive analytics.",
    },
    {
      icon: "🏥",
      title: "Healthcare AI Automation",
      desc: "Advanced infrastructure for hospitals, diagnostics, patient workflows, and medical operations.",
    },
  ];

  const industries = [
    "Healthcare",
    "Hospitals",
    "SaaS",
    "Startups",
    "Agencies",
    "Real Estate",
    "Education",
    "E-Commerce",
  ];

  return (
    <div className="min-h-screen bg-[#02040a] text-white overflow-x-hidden selection:bg-cyan-400 selection:text-black">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[700px] h-[700px] bg-cyan-500/20 blur-[160px] rounded-full" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[700px] h-[700px] bg-purple-500/20 blur-[160px] rounded-full" />
      </div>

      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-2xl border-b border-white/10 bg-black/40">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-cyan-400">
              PhantomOpsAI
            </h1>
            <p className="text-zinc-500 text-sm mt-1">
              Autonomous AI Infrastructure Platform
            </p>
          </div>

          <div className="hidden md:flex items-center gap-8 text-sm text-zinc-400">
            <a href="#services" className="hover:text-white transition">Services</a>
            <a href="#capabilities" className="hover:text-white transition">Capabilities</a>
            <a href="#industries" className="hover:text-white transition">Industries</a>
            <a href="#contact" className="hover:text-white transition">Contact</a>
          </div>

          <div className="flex items-center gap-4">
            <button className="px-5 py-3 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-300">
              Open CRM
            </button>

            <button className="px-5 py-3 rounded-2xl bg-cyan-500 hover:bg-cyan-400 hover:scale-105 transition-all duration-300 text-black font-black shadow-[0_0_50px_rgba(34,211,238,0.45)]">
              Book Consultation →
            </button>
          </div>
        </div>
      </nav>

      <section className="relative min-h-screen flex items-center justify-center px-6 pt-40">
        <div className="max-w-7xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full border border-green-500/20 bg-green-500/5 text-green-400 uppercase tracking-[0.25em] text-xs mb-10 animate-pulse">
            <div className="w-2 h-2 rounded-full bg-green-400" />
            Autonomous AI Infrastructure Platform — Online
          </div>

          <h1 className="text-6xl md:text-8xl font-black leading-[0.9] tracking-tight">
            Building AI
            <span className="block text-cyan-400">
              Business Systems
            </span>
            <span className="block text-zinc-500 text-4xl md:text-5xl mt-6">
              That Operate 24/7 — Without You
            </span>
          </h1>

          <p className="max-w-4xl mx-auto text-zinc-400 text-xl md:text-2xl leading-relaxed mt-12">
            PhantomOps AI builds autonomous commercial intelligence systems,
            AI workflow automation, CRM infrastructure, revenue analytics,
            and healthcare automation platforms for modern businesses.
          </p>

          <div className="flex flex-wrap justify-center gap-5 mt-16">
            <button className="px-10 py-5 rounded-3xl bg-cyan-500 hover:bg-cyan-400 hover:scale-105 transition-all duration-300 text-black font-black text-lg shadow-[0_0_80px_rgba(34,211,238,0.5)]">
              Start Automation
            </button>

            <button className="px-10 py-5 rounded-3xl border border-white/10 bg-white/5 hover:bg-white/10 hover:scale-105 transition-all duration-300 font-bold text-lg">
              View Demo
            </button>
          </div>

          <div className="grid md:grid-cols-4 gap-6 mt-28">
            {[
              ["AI", "Commercial Intelligence", "text-cyan-400"],
              ["CRM", "Revenue Operations", "text-green-400"],
              ["24/7", "Autonomous Runtime", "text-purple-400"],
              ["∞", "Scalable Infrastructure", "text-yellow-400"],
            ].map((item, index) => (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-[32px] p-8 backdrop-blur-xl hover:border-cyan-400/30 transition-all duration-300 hover:-translate-y-2"
              >
                <h3 className={`text-6xl font-black ${item[2]}`}>
                  {item[0]}
                </h3>
                <p className="text-zinc-400 text-lg mt-4">
                  {item[1]}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="capabilities" className="px-6 py-32 relative z-10">
        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-10 items-start">
          <div className="bg-[#060912] border border-white/10 rounded-[40px] p-10 shadow-2xl">
            <div className="flex items-center justify-between mb-10">
              <div>
                <p className="text-cyan-400 uppercase tracking-[0.25em] text-xs">
                  AI Runtime Status
                </p>
                <h2 className="text-5xl font-black mt-4">
                  LIVE
                </h2>
              </div>

              <div className="w-4 h-4 rounded-full bg-green-400 animate-pulse" />
            </div>

            <div className="space-y-5">
              {runtime.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between border-b border-white/5 pb-4"
                >
                  <span className="text-zinc-400 text-lg">
                    {item[0]}
                  </span>

                  <span className="text-green-400 font-bold tracking-wide">
                    {item[1]}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-black border border-white/10 rounded-[40px] p-10 overflow-hidden relative shadow-2xl">
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5" />

            <div className="relative z-10 font-mono text-sm md:text-base text-green-400 space-y-2 leading-relaxed">
              <p className="text-zinc-500">
                phantomops-ai — runtime core v2.8.4
              </p>

              <p>$ phantomops start --mode autonomous --all</p>
              <p>✓ Booting AI runtime kernel...</p>
              <p>→ CRM intelligence module loaded</p>
              <p>→ Marketplace scanner: ONLINE (400+ sources)</p>
              <p>→ Proposal engine: ARMED</p>
              <p>→ Revenue tracker: LIVE</p>
              <p>✓ Inbox monitor: watching 3 accounts</p>
              <p>⚡ Opportunity detected: Enterprise RFP</p>
              <p>→ Generating AI proposal...</p>
              <p>✓ Proposal sent in 4.2s</p>
              <p>⚡ Lead scored: HIGH PRIORITY (94%)</p>
              <p>→ Autonomous followup: scheduled T+24h</p>

              <div className="pt-8">
                <p>$ phantomops status</p>
                <p>✓ All systems OPERATIONAL</p>
                <p>Runtime: 847h 22m continuous</p>
                <p>Efficiency: 98.4% | Leads processed: 12,847</p>
                <p className="animate-pulse">$</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="services" className="px-6 py-32 bg-[#050816] relative z-10">
        <div className="max-w-7xl mx-auto">
          <div className="mb-20">
            <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
              Services
            </p>

            <h2 className="text-6xl font-black leading-none">
              Enterprise AI
              <span className="block text-zinc-500 mt-4">
                Infrastructure
              </span>
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <div
                key={index}
                className="group bg-white/5 border border-white/10 rounded-[36px] p-10 hover:border-cyan-400/30 hover:-translate-y-3 transition-all duration-500"
              >
                <div className="text-6xl mb-10 group-hover:scale-110 transition-transform duration-300">
                  {service.icon}
                </div>

                <h3 className="text-3xl font-black leading-tight mb-6">
                  {service.title}
                </h3>

                <p className="text-zinc-400 text-lg leading-relaxed mb-10">
                  {service.desc}
                </p>

                <div className="inline-flex items-center gap-2 text-cyan-400 font-bold tracking-wide uppercase text-sm">
                  <div className="w-2 h-2 rounded-full bg-cyan-400" />
                  24/7 Runtime
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="industries" className="px-6 py-32 relative z-10">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
            Industries
          </p>

          <h2 className="text-6xl font-black leading-none mb-20">
            Built For
            <span className="block text-zinc-500 mt-4">
              High-Impact Industries
            </span>
          </h2>

          <div className="grid md:grid-cols-4 gap-6">
            {industries.map((industry, index) => (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-[32px] p-10 hover:border-cyan-400/30 hover:-translate-y-2 transition-all duration-300"
              >
                <h3 className="text-2xl font-black">
                  {industry}
                </h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="contact" className="px-6 py-32 bg-[#050816] relative z-10">
        <div className="max-w-5xl mx-auto bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-white/10 rounded-[48px] p-16 text-center shadow-[0_0_120px_rgba(34,211,238,0.08)]">
          <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
            Start Building
          </p>

          <h2 className="text-6xl font-black leading-none">
            Build Your AI
            <span className="block text-zinc-500 mt-4">
              Infrastructure Today.
            </span>
          </h2>

          <p className="text-zinc-400 text-xl leading-relaxed max-w-3xl mx-auto mt-10">
            Deploy autonomous AI systems that automate workflows,
            optimize revenue operations, and scale business intelligence.
            Your business, running itself.
          </p>

          <div className="flex flex-wrap justify-center gap-5 mt-14">
            <button className="px-10 py-5 rounded-3xl bg-cyan-500 hover:bg-cyan-400 hover:scale-105 transition-all duration-300 text-black font-black text-lg shadow-[0_0_60px_rgba(34,211,238,0.45)]">
              Request Consultation
            </button>

            <button className="px-10 py-5 rounded-3xl border border-white/10 bg-white/5 hover:bg-white/10 hover:scale-105 transition-all duration-300 font-bold text-lg">
              Explore Capabilities
            </button>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/10 bg-black px-6 py-10 relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-5">
          <div>
            <h2 className="text-3xl font-black text-cyan-400">
              PhantomOpsAI
            </h2>

            <p className="text-zinc-500 text-sm mt-2">
              Autonomous AI Operations Infrastructure
            </p>
          </div>

          <div className="flex gap-6 text-zinc-500 text-sm">
            <a href="#services" className="hover:text-white transition">Services</a>
            <a href="#capabilities" className="hover:text-white transition">Capabilities</a>
            <a href="#industries" className="hover:text-white transition">Industries</a>
            <a href="#contact" className="hover:text-white transition">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
