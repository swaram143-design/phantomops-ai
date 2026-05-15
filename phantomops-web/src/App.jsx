import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function PhantomOpsInteractive() {
  const [showCRM, setShowCRM] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [logs, setLogs] = useState([
    "✓ AI runtime initialized",
    "→ Marketplace scanner ONLINE",
    "✓ CRM intelligence loaded",
    "⚡ Opportunity signal detected",
  ]);

  useEffect(() => {
    const runtimeLogs = [
      "✓ Proposal generated in 4.2s",
      "→ Lead scored HIGH PRIORITY",
      "✓ Revenue analytics synchronized",
      "⚡ AI detected enterprise inquiry",
      "→ Autonomous followup scheduled",
      "✓ Telegram automation active",
      "→ Inbox monitor scanning accounts",
    ];

    const interval = setInterval(() => {
      setLogs((prev) => {
        const next = runtimeLogs[Math.floor(Math.random() * runtimeLogs.length)];
        return [...prev.slice(-6), next];
      });
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  const scrollToSection = (id) => {
    const el = document.getElementById(id);

    if (el) {
      el.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#02040a] text-white overflow-x-hidden">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <motion.div
          animate={{
            x: [0, 40, 0],
            y: [0, -30, 0],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
          }}
          className="absolute top-[-10%] left-[-10%] w-[700px] h-[700px] bg-cyan-500/20 blur-[180px] rounded-full"
        />

        <motion.div
          animate={{
            x: [0, -30, 0],
            y: [0, 40, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
          }}
          className="absolute bottom-[-10%] right-[-10%] w-[700px] h-[700px] bg-purple-500/20 blur-[180px] rounded-full"
        />
      </div>

      <nav className="fixed top-0 left-0 right-0 z-50 bg-black/40 backdrop-blur-2xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-black text-cyan-400 tracking-tight">
              PhantomOpsAI
            </h1>

            <p className="text-zinc-500 text-sm mt-1">
              Autonomous AI Infrastructure Platform
            </p>
          </div>

          <div className="hidden md:flex items-center gap-8 text-zinc-400 text-sm">
            <button onClick={() => scrollToSection("services")} className="hover:text-white transition">
              Services
            </button>

            <button onClick={() => scrollToSection("runtime")} className="hover:text-white transition">
              Runtime
            </button>

            <button onClick={() => scrollToSection("industries")} className="hover:text-white transition">
              Industries
            </button>

            <button onClick={() => scrollToSection("contact")} className="hover:text-white transition">
              Contact
            </button>
          </div>

          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => setShowCRM(true)}
              className="px-5 py-3 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 transition"
            >
              Open CRM
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.96 }}
              onClick={() => setShowModal(true)}
              className="px-5 py-3 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black shadow-[0_0_60px_rgba(34,211,238,0.4)]"
            >
              Book Consultation →
            </motion.button>
          </div>
        </div>
      </nav>

      <AnimatePresence>
        {showCRM && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/90 backdrop-blur-xl overflow-y-auto"
          >
            <div className="max-w-7xl mx-auto p-10">
              <div className="flex items-center justify-between mb-10">
                <div>
                  <h2 className="text-5xl font-black text-cyan-400">
                    PhantomOps CRM
                  </h2>

                  <p className="text-zinc-400 mt-3">
                    Autonomous Revenue Operations Dashboard
                  </p>
                </div>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowCRM(false)}
                  className="px-5 py-3 rounded-2xl bg-red-500 hover:bg-red-400"
                >
                  Exit Dashboard
                </motion.button>
              </div>

              <div className="grid md:grid-cols-4 gap-6 mb-10">
                {[
                  ["Leads", "127", "text-cyan-400"],
                  ["AI Runtime", "LIVE", "text-green-400"],
                  ["Automation", "ACTIVE", "text-purple-400"],
                  ["Revenue", "$48K", "text-yellow-400"],
                ].map((card, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white/5 border border-white/10 rounded-[32px] p-8"
                  >
                    <p className="text-zinc-500 uppercase tracking-[0.2em] text-xs">
                      {card[0]}
                    </p>

                    <h3 className={`text-5xl font-black mt-5 ${card[2]}`}>
                      {card[1]}
                    </h3>
                  </motion.div>
                ))}
              </div>

              <div className="bg-white/5 border border-white/10 rounded-[40px] p-8 overflow-x-auto">
                <table className="w-full text-left min-w-[900px]">
                  <thead>
                    <tr className="border-b border-white/10 text-zinc-500 uppercase tracking-[0.2em] text-xs">
                      <th className="p-5">Lead</th>
                      <th className="p-5">Company</th>
                      <th className="p-5">Status</th>
                      <th className="p-5">Priority</th>
                      <th className="p-5">AI Score</th>
                    </tr>
                  </thead>

                  <tbody>
                    {[
                      ["Mahalaxmi", "Healthcare", "Proposal Sent", "HIGH", "94%"],
                      ["Vision Labs", "SaaS", "AI Followup", "MEDIUM", "88%"],
                      ["Apollo Ops", "Hospitals", "Contacted", "HIGH", "97%"],
                    ].map((lead, index) => (
                      <tr key={index} className="border-b border-white/5 hover:bg-white/5 transition">
                        <td className="p-5">{lead[0]}</td>
                        <td className="p-5 text-zinc-400">{lead[1]}</td>
                        <td className="p-5 text-cyan-400">{lead[2]}</td>
                        <td className="p-5 text-yellow-400">{lead[3]}</td>
                        <td className="p-5 text-green-400 font-bold">{lead[4]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-xl flex items-center justify-center p-6"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="w-full max-w-2xl bg-[#060912] border border-white/10 rounded-[40px] p-10"
            >
              <div className="flex items-center justify-between mb-10">
                <div>
                  <h2 className="text-4xl font-black text-cyan-400">
                    Request Consultation
                  </h2>

                  <p className="text-zinc-400 mt-3">
                    Deploy autonomous AI infrastructure for your business.
                  </p>
                </div>

                <button
                  onClick={() => setShowModal(false)}
                  className="text-zinc-500 hover:text-white text-3xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-6">
                <input
                  placeholder="Full Name"
                  className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400"
                />

                <input
                  placeholder="Email Address"
                  className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400"
                />

                <input
                  placeholder="Company Name"
                  className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400"
                />

                <textarea
                  rows="5"
                  placeholder="Describe your automation requirements"
                  className="w-full bg-black/50 border border-white/10 rounded-2xl px-6 py-5 outline-none focus:border-cyan-400"
                />

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black text-lg shadow-[0_0_80px_rgba(34,211,238,0.4)]"
                >
                  Launch AI Infrastructure
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <section className="min-h-screen flex items-center justify-center px-6 pt-40 relative z-10">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
          >
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full border border-green-500/20 bg-green-500/5 text-green-400 uppercase tracking-[0.25em] text-xs mb-10">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
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
          </motion.div>
        </div>
      </section>
    </div>
  );
}
