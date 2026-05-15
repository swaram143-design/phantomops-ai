export default function RuntimeGrid() {
  const stats = [
    {
      title: "AI Runtime",
      value: "LIVE",
      color: "text-green-400"
    },
    {
      title: "Automation",
      value: "ACTIVE",
      color: "text-cyan-400"
    },
    {
      title: "AI Agents",
      value: "READY",
      color: "text-purple-400"
    },
    {
      title: "Infrastructure",
      value: "24/7",
      color: "text-yellow-400"
    }
  ];

  return (
    <section className="px-6 pb-24 -mt-24 relative z-20">
      <div className="max-w-7xl mx-auto grid md:grid-cols-4 gap-6">

        {stats.map((item, index) => (
          <div
            key={index}
            className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8"
          >
            <p className="text-zinc-500 text-sm uppercase tracking-[0.2em]">
              {item.title}
            </p>

            <h3 className={`text-5xl font-black mt-6 ${item.color}`}>
              {item.value}
            </h3>
          </div>
        ))}

      </div>
    </section>
  );
}
