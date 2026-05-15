export default function Services() {
  const services = [
    {
      title: "Autonomous CRM",
      desc: "AI-powered CRM operations with lead intelligence, proposal automation, and analytics."
    },
    {
      title: "Healthcare AI",
      desc: "Advanced medical workflow systems, diagnostics automation, and hospital operations."
    },
    {
      title: "Revenue Systems",
      desc: "Commercial intelligence pipelines, outreach automation, and revenue optimization."
    }
  ];

  return (
    <section className="px-6 py-32 bg-[#050816]">
      <div className="max-w-7xl mx-auto">

        <div className="mb-20">
          <p className="text-cyan-400 uppercase tracking-[0.25em] text-xs mb-5">
            Enterprise Services
          </p>

          <h2 className="text-6xl font-black leading-none">
            AI Systems That Scale Operations
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">

          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white/5 border border-white/10 rounded-[32px] p-10 hover:border-cyan-400/30 transition"
            >

              <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 mb-8 flex items-center justify-center">
                <div className="w-6 h-6 rounded-full bg-cyan-400" />
              </div>

              <h3 className="text-3xl font-black mb-6">
                {service.title}
              </h3>

              <p className="text-zinc-400 text-lg leading-relaxed">
                {service.desc}
              </p>

            </div>
          ))}

        </div>

      </div>
    </section>
  );
}
