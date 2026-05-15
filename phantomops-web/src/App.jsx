import React, { useState } from "react";
import { motion } from "framer-motion";

export default function App() {
const [showCRM, setShowCRM] = useState(false);

const scrollToSection = (id) => {
const element = document.getElementById(id);

if (element) {
  element.scrollIntoView({
    behavior: "smooth",
  });
}

};

return (
<div className="min-h-screen bg-[#02040a] text-white overflow-x-hidden">

  {/* BACKGROUND */}
  <div className="fixed inset-0 z-0 overflow-hidden">

    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#0f172a,transparent_60%)]" />

    <div className="absolute inset-0 opacity-20">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:80px_80px]" />
    </div>

  </div>

  {/* NAVBAR */}
  <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/30 backdrop-blur-2xl">

    <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">

      <div>
        <h1 className="text-2xl font-black tracking-tight">
          PhantomOpsAI
        </h1>

        <p className="text-xs text-zinc-500 mt-1">
          Autonomous AI Infrastructure Platform
        </p>
      </div>

      <div className="hidden md:flex items-center gap-10 text-sm text-zinc-300">

        <button onClick={() => scrollToSection("products")}>
          Products
        </button>

        <button onClick={() => scrollToSection("runtime")}>
          Runtime
        </button>

        <button onClick={() => scrollToSection("industries")}>
          Industries
        </button>

      </div>

      <div className="flex gap-3">

        <button
          onClick={() => setShowCRM(true)}
          className="px-5 py-3 rounded-2xl border border-cyan-400/30 bg-cyan-400/10 hover:bg-cyan-400/20 transition-all"
        >
          Open CRM
        </button>

        <button className="px-5 py-3 rounded-2xl bg-white text-black font-bold hover:scale-105 transition-all">
          Book Consultation
        </button>

      </div>

    </div>

  </nav>

  {/* HERO */}
  <section className="relative z-10 min-h-screen flex items-center px-6 pt-40 pb-24">

    <div className="max-w-7xl mx-auto w-full grid lg:grid-cols-2 gap-20 items-center">

      <div>

        <div className="inline-flex items-center gap-3 border border-cyan-500/20 bg-cyan-500/10 rounded-full px-5 py-2 mb-10">

          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />

          <span className="text-sm text-cyan-300">
            Autonomous AI Infrastructure Platform — Online
          </span>

        </div>

        <h1 className="text-7xl lg:text-8xl font-black leading-none tracking-tight">

          Building AI

          <span className="block text-zinc-500 mt-4">
            Business Systems
          </span>

          <span className="block mt-4">
            That Operate 24/7
          </span>

        </h1>

        <p className="text-zinc-400 text-xl leading-relaxed mt-10 max-w-2xl">
          PhantomOps AI builds autonomous commercial intelligence systems,
          CRM infrastructure, healthcare AI automation, outreach engines,
          and operational AI runtimes for modern businesses.
        </p>

        <div className="flex flex-wrap gap-5 mt-14">

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-5 rounded-3xl bg-cyan-400 text-black font-black shadow-[0_0_60px_rgba(34,211,238,0.35)]"
          >
            Start Automation
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => scrollToSection("products")}
            className="px-8 py-5 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl"
          >
            View Live Products
          </motion.button>

        </div>

      </div>

      {/* TERMINAL */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="relative"
      >

        <div className="absolute -inset-8 bg-cyan-500/10 blur-3xl rounded-full" />

        <div className="relative bg-black/60 border border-cyan-500/20 rounded-[32px] overflow-hidden backdrop-blur-2xl">

          <div className="flex items-center gap-3 px-6 py-4 border-b border-white/10">

            <div className="w-3 h-3 rounded-full bg-red-400" />
            <div className="w-3 h-3 rounded-full bg-yellow-400" />
            <div className="w-3 h-3 rounded-full bg-green-400" />

            <p className="ml-4 text-sm text-zinc-400">
              gram-runtime v1.0.0
            </p>

          </div>

          <div className="p-8 font-mono text-sm space-y-4 text-zinc-300">

            <p className="text-cyan-400">
              $ gram boot --autonomous --all
            </p>

            <p>✓ GRAM Runtime initialized</p>
            <p>→ RevenueOps agent ONLINE</p>
            <p>→ MediOps agent ONLINE</p>
            <p>→ Outreach agent ONLINE</p>
            <p>✓ Autonomous orchestration active</p>
            <p>⚡ Opportunity signal detected</p>
            <p>✓ Proposal generated</p>
            <p>→ Followup automation scheduled</p>

          </div>

        </div>

      </motion.div>

    </div>

  </section>

  {/* PRODUCTS */}
  <section
    id="products"
    className="relative z-10 px-6 py-32"
  >

    <div className="max-w-7xl mx-auto">

      <div className="text-center mb-20">

        <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
          Live AI Products
        </p>

        <h2 className="text-6xl font-black leading-none">

          Autonomous AI

          <span className="block text-zinc-500 mt-4">
            Infrastructure Systems
          </span>

        </h2>

        <p className="text-zinc-400 text-xl max-w-4xl mx-auto mt-10 leading-relaxed">
          Production-grade autonomous systems currently operating inside
          the PhantomOps runtime infrastructure.
        </p>

      </div>

      <div className="grid lg:grid-cols-2 gap-8">

        {[
          {
            title: "PhantomOps CRM Intelligence",
            status: "LIVE",
            features: [
              "AI lead scoring",
              "Proposal generation",
              "Autonomous followups",
              "Revenue analytics",
              "CRM automation",
            ],
            primary: "Open Dashboard",
            secondary: "View Runtime",
          },
          {
            title: "MediOps AI",
            status: "HEALTHCARE ACTIVE",
            features: [
              "Patient workflows",
              "Triage automation",
              "Diagnostics support",
              "Hospital admin AI",
              "Medical automation",
            ],
            primary: "Explore System",
            secondary: "View Medical Runtime",
          },
          {
            title: "Outreach AI",
            status: "AUTOMATION ACTIVE",
            features: [
              "AI cold outreach",
              "Telegram automation",
              "WhatsApp AI",
              "Marketplace scanning",
              "Proposal generation",
            ],
            primary: "Launch Outreach",
            secondary: "Watch AI Pipeline",
          },
          {
            title: "GRAM Runtime",
            status: "ORCHESTRATION READY",
            features: [
              "Multi-agent hierarchy",
              "Autonomous orchestration",
              "Voice runtime",
              "AI task delegation",
              "Operational intelligence",
            ],
            primary: "Open Runtime",
            secondary: "View Agents",
          },
        ].map((item, index) => (

          <motion.div
            key={index}
            whileHover={{ y: -10 }}
            className="bg-white/5 border border-white/10 rounded-[40px] p-10 backdrop-blur-2xl hover:border-cyan-400/30 transition-all duration-500"
          >

            <div className="flex items-center justify-between mb-8">

              <div>

                <p className="text-cyan-400 uppercase text-xs tracking-[0.25em]">
                  {item.status}
                </p>

                <h3 className="text-4xl font-black mt-4">
                  {item.title}
                </h3>

              </div>

              <div className="w-4 h-4 rounded-full bg-green-400 animate-pulse" />

            </div>

            <div className="space-y-4 text-zinc-300 text-lg">

              {item.features.map((feature, i) => (
                <p key={i}>✓ {feature}</p>
              ))}

            </div>

            <div className="mt-10 flex flex-wrap gap-4">

              <button
                onClick={() => setShowCRM(true)}
                className="px-6 py-4 rounded-2xl bg-cyan-400 text-black font-black"
              >
                {item.primary}
              </button>

              <button className="px-6 py-4 rounded-2xl border border-white/10 bg-white/5">
                {item.secondary}
              </button>

            </div>

          </motion.div>

        ))}

      </div>

    </div>

  </section>

  {/* RUNTIME */}
  <section
    id="runtime"
    className="relative z-10 px-6 py-32"
  >

    <div className="max-w-7xl mx-auto">

      <div className="grid md:grid-cols-4 gap-6">

        {[
          ["AI Runtime", "LIVE"],
          ["Marketplace Intelligence", "ACTIVE"],
          ["CRM Analytics", "ACTIVE"],
          ["Proposal Engine", "ARMED"],
        ].map((item, index) => (

          <div
            key={index}
            className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl"
          >

            <p className="text-zinc-500 text-sm">
              {item[0]}
            </p>

            <h3 className="text-3xl font-black mt-4 text-cyan-400">
              {item[1]}
            </h3>

          </div>

        ))}

      </div>

    </div>

  </section>

  {/* INDUSTRIES */}
  <section
    id="industries"
    className="relative z-10 px-6 py-32"
  >

    <div className="max-w-7xl mx-auto text-center">

      <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
        Industries
      </p>

      <h2 className="text-6xl font-black">
        Built For High-Impact Industries
      </h2>

      <div className="grid md:grid-cols-4 gap-6 mt-20">

        {[
          "Healthcare",
          "Hospitals",
          "SaaS",
          "Startups",
          "Agencies",
          "Education",
          "Real Estate",
          "E-Commerce",
        ].map((item, index) => (

          <div
            key={index}
            className="bg-white/5 border border-white/10 rounded-3xl p-8 text-xl font-bold"
          >
            {item}
          </div>

        ))}

      </div>

    </div>

  </section>

  {/* FOOTER */}
  <footer className="relative z-10 border-t border-white/10 px-6 py-12">

    <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between gap-8">

      <div>

        <h2 className="text-3xl font-black">
          PhantomOpsAI
        </h2>

        <p className="text-zinc-500 mt-3">
          Autonomous AI Operations Infrastructure
        </p>

      </div>

      <div className="text-zinc-500">
        © 2026 PhantomOps AI. All rights reserved.
      </div>

    </div>

  </footer>

  {/* CRM MODAL */}
  {showCRM && (

    <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-xl flex items-center justify-center p-6">

      <div className="bg-[#0b1120] border border-cyan-500/20 rounded-[32px] max-w-4xl w-full p-10 relative">

        <button
          onClick={() => setShowCRM(false)}
          className="absolute top-5 right-5 text-zinc-400 hover:text-white"
        >
          ✕
        </button>

        <h2 className="text-4xl font-black mb-10">
          PhantomOps CRM
        </h2>

        <div className="overflow-auto">

          <table className="w-full text-left">

            <thead>

              <tr className="border-b border-white/10">

                <th className="p-5">Name</th>
                <th className="p-5">Email</th>
                <th className="p-5">Company</th>
                <th className="p-5">Requirement</th>

              </tr>

            </thead>

            <tbody>

              <tr className="border-b border-white/5">

                <td className="p-5">Ramesh</td>
                <td className="p-5 text-cyan-400">
                  demo@phantomops.ai
                </td>
                <td className="p-5">PhantomOps</td>
                <td className="p-5">
                  Autonomous AI Infrastructure
                </td>

              </tr>

              <tr className="border-b border-white/5">

                <td className="p-5">Healthcare Lead</td>
                <td className="p-5 text-cyan-400">
                  hospital@med.ai
                </td>
                <td className="p-5">MediOps</td>
                <td className="p-5">
                  Hospital AI Automation
                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  )}

</div>

);
}