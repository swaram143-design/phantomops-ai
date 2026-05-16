import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

export default function App() {
const [showCRM, setShowCRM] = useState(false);
const [showLeadModal, setShowLeadModal] = useState(false);

const [leadData, setLeadData] = useState({
  name: "",
  email: "",
  company: "",
  requirement: "",
});
const [mobileMenu, setMobileMenu] = useState(false);

const [proposalGenerated, setProposalGenerated] = useState(false);

const [proposalLoading, setProposalLoading] = useState(false);

const [proposalData, setProposalData] = useState({
  company: "",
  requirement: "",
  budget: "",
});

const triggerProposal = (system) => {

  setProposalLoading(true);

  setProposalGenerated(false);

 let requirement = "Autonomous AI Infrastructure";

if (system === "PhantomOps CRM Intelligence") {
  requirement = "CRM Analytics & Revenue Automation";
}

if (system === "MediOps AI") {
  requirement = "Hospital AI Workflow Infrastructure";
}

if (system === "Outreach AI") {
  requirement = "AI Outreach & Marketplace Automation";
}

if (system === "GRAM Runtime") {
  requirement = "Multi-Agent Runtime Orchestration";
}

setProposalData({
  company: system,
  requirement,
  budget: "$50k - $100k",
});

  const proposalSection = document.getElementById("proposal-runtime");

if (proposalSection) {

  proposalSection.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });

}

  setTimeout(() => {

    setProposalLoading(false);

    setProposalGenerated(true);

  }, 2200);

};

const scrollToSection = (id) => {

  const element = document.getElementById(id);

  if (element) {

    element.scrollIntoView({
      behavior: "smooth",
    });

  }

};

return (
<div className="relative min-h-screen bg-[#02040a] text-white overflow-x-hidden">
{/* AMBIENT BACKGROUND */}

<div className="absolute inset-0 overflow-hidden pointer-events-none">

  <div className="absolute top-[-200px] left-[-100px] w-[500px] h-[500px] rounded-full bg-cyan-500/10 blur-[140px] animate-pulse" />

  <div className="absolute bottom-[-200px] right-[-100px] w-[500px] h-[500px] rounded-full bg-blue-500/10 blur-[140px] animate-pulse" />

  <div className="absolute top-[40%] left-[50%] -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full bg-cyan-400/5 blur-[120px]" />

</div>

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
<button
  onClick={() => setMobileMenu(!mobileMenu)}
  className="md:hidden flex flex-col gap-1.5"
>

  <span className="w-7 h-[2px] bg-white rounded-full" />
  <span className="w-7 h-[2px] bg-white rounded-full" />
  <span className="w-7 h-[2px] bg-white rounded-full" />

</button>

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

      <div className="hidden md:flex gap-3">

      <button
  onClick={() => setShowCRM(true)}
  className="group relative overflow-hidden px-5 py-3 rounded-2xl border border-cyan-400/30 bg-cyan-400/10 hover:bg-cyan-400/20 hover:scale-[1.03] transition-all duration-300 hover:shadow-[0_0_35px_rgba(34,211,238,0.35)]"
>

  <span className="relative z-10">
    Open CRM
  </span>

  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.45),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

</button>

      <a
  href="https://wa.me/919177334156?text=Hello%20PhantomOps%20AI%2C%20I%20want%20to%20book%20a%20consultation."
  target="_blank"
  rel="noopener noreferrer"
  className="group relative overflow-hidden px-5 py-3 rounded-2xl bg-white text-black font-bold hover:scale-[1.03] transition-all duration-300 hover:shadow-[0_0_40px_rgba(255,255,255,0.25)]"
>

  <span className="relative z-10">
    Book Consultation
  </span>

  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.5),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

</a>

</div>

</div>

{mobileMenu && (

  <motion.div
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    className="md:hidden absolute top-full left-0 right-0 border-b border-white/10 bg-black/95 backdrop-blur-2xl"
  >

    <div className="flex flex-col p-6 gap-5">

      <button
        onClick={() => {
          scrollToSection("products");
          setMobileMenu(false);
        }}
        className="text-left text-white text-lg"
      >
        Products
      </button>

      <button
        onClick={() => {
          scrollToSection("runtime");
          setMobileMenu(false);
        }}
        className="text-left text-white text-lg"
      >
        Runtime
      </button>

      <button
        onClick={() => {
          scrollToSection("industries");
          setMobileMenu(false);
        }}
        className="text-left text-white text-lg"
      >
        Industries
      </button>

      <button
        onClick={() => {
          setShowCRM(true);
          setMobileMenu(false);
        }}
        className="mt-4 px-5 py-4 rounded-2xl bg-cyan-400 text-black font-black"
      >
        Open CRM
      </button>

      <a
        href="https://wa.me/919177334156?text=Hello%20PhantomOps%20AI%2C%20I%20want%20to%20book%20a%20consultation."
        target="_blank"
        rel="noopener noreferrer"
        className="px-5 py-4 rounded-2xl bg-white text-black font-black text-center"
      >
        Book Consultation
      </a>

    </div>

  </motion.div>

)}

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
  whileHover={{ scale: 1.03 }}
  whileTap={{ scale: 0.97 }}
  className="group relative overflow-hidden px-8 py-5 rounded-3xl bg-cyan-400 text-black font-black shadow-[0_0_60px_rgba(34,211,238,0.35)] hover:shadow-[0_0_90px_rgba(34,211,238,0.55)] transition-all duration-300"
>

  <span className="relative z-10">
    Start Automation
  </span>

  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.55),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

</motion.button>

         <motion.button
  onClick={() => setShowLeadModal(true)}
  whileHover={{ scale: 1.03 }}
  whileTap={{ scale: 0.97 }}
  onClick={() => scrollToSection("products")}
  className="group relative overflow-hidden px-8 py-5 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:border-cyan-400/40 hover:bg-cyan-400/10 transition-all duration-300"
>

  <span className="relative z-10">
    View Live Products
  </span>

  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.2),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

</motion.button>

        </div>

      </div>

<div className="grid grid-cols-2 lg:grid-cols-4 gap-5 mt-16">

  {[
    ["98%", "Automation Efficiency"],
    ["12,847", "Leads Processed"],
    ["24/7", "Runtime Stability"],
    ["400+", "Marketplace Sources"],
  ].map((item, index) => (

    <motion.div
      key={index}
      whileHover={{ y: -6 }}
      transition={{ duration: 0.2 }}
      className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl p-6 group"
    >

      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-transparent opacity-60 group-hover:opacity-100 transition-all duration-500" />

      <div className="relative z-10">

        <h3 className="text-4xl font-black text-cyan-400">
          {item[0]}
        </h3>

        <p className="text-zinc-400 text-sm mt-3">
          {item[1]}
        </p>

      </div>

    </motion.div>

  ))}

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
            whileHover={{
  y: -8,
  scale: 1.015,
}}
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
    onClick={() => triggerProposal(item.title)}
    className="group relative overflow-hidden px-6 py-4 rounded-2xl bg-cyan-400 text-black font-black hover:scale-[1.03] transition-all duration-300"
  >

    <span className="relative z-10">
      {item.primary}
    </span>

    <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.45),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

  </button>

  <button
    className="px-6 py-4 rounded-2xl border border-white/10 bg-white/5 hover:border-cyan-400/30 transition-all duration-300"
  >
    {item.secondary}
  </button>

</div>

          </motion.div>

        ))}

      </div>

    </div>

  </section>

<section className="relative z-10 px-6 py-28">

  <div className="max-w-7xl mx-auto">

    <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-10 mb-16">

      <div>

        <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
          Autonomous Runtime Activity
        </p>

        <h2 className="text-5xl lg:text-6xl font-black leading-none">

          Live AI
          <span className="block text-zinc-500 mt-3">
            Operational Feed
          </span>

        </h2>

      </div>

      <div className="flex items-center gap-4 px-6 py-4 rounded-2xl border border-green-500/20 bg-green-500/10 backdrop-blur-xl">

        <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse" />

        <span className="text-green-300 text-sm font-medium">
          Runtime Infrastructure Active
        </span>

      </div>

    </div>

    <div className="grid lg:grid-cols-2 gap-8">

      <div className="bg-white/5 border border-white/10 rounded-[36px] p-8 backdrop-blur-2xl">

        <div className="space-y-5 font-mono text-sm">

          {[
            "✓ Enterprise proposal generated successfully",
            "✓ AI outreach pipeline launched",
            "✓ Marketplace signal detected",
            "✓ Revenue analytics synchronized",
            "✓ CRM followup automation scheduled",
            "✓ WhatsApp campaign deployed",
            "✓ Lead score increased to 94%",
            "✓ Autonomous runtime stabilized",
          ].map((item, index) => (

            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{
                duration: 0.4,
                delay: index * 0.08,
              }}
              className="flex items-center gap-4 p-4 rounded-2xl border border-white/5 bg-black/20"
            >

              <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />

              <p className="text-zinc-300">
                {item}
              </p>

            </motion.div>

          ))}

        </div>

      </div>

      <div className="grid gap-6">

        <motion.div
          whileHover={{ y: -5 }}
          className="relative overflow-hidden rounded-[36px] border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 to-transparent p-8 backdrop-blur-2xl"
        >

          <div className="absolute inset-0 opacity-40 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.3),transparent_70%)]" />

          <div className="relative z-10">

            <p className="text-zinc-500 text-sm">
              Runtime Uptime
            </p>

            <h3 className="text-6xl font-black mt-4">
              847h
            </h3>

            <p className="text-cyan-300 mt-4">
              Continuous autonomous runtime
            </p>

          </div>

        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="relative overflow-hidden rounded-[36px] border border-purple-500/20 bg-gradient-to-br from-purple-500/10 to-transparent p-8 backdrop-blur-2xl"
        >

          <div className="relative z-10">

            <p className="text-zinc-500 text-sm">
              AI Proposal Speed
            </p>

            <h3 className="text-6xl font-black mt-4">
              4.2s
            </h3>

            <p className="text-purple-300 mt-4">
              Average generation runtime
            </p>

          </div>

        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="relative overflow-hidden rounded-[36px] border border-green-500/20 bg-gradient-to-br from-green-500/10 to-transparent p-8 backdrop-blur-2xl"
        >

          <div className="relative z-10">

            <p className="text-zinc-500 text-sm">
              Runtime Efficiency
            </p>

            <h3 className="text-6xl font-black mt-4">
              98.4%
            </h3>

            <p className="text-green-300 mt-4">
              AI automation optimization
            </p>

          </div>

        </motion.div>

      </div>

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

{/* AI PROPOSAL GENERATOR */}

<section
  id="proposal-runtime"
  className="relative z-10 px-6 py-32"
>

  <div className="max-w-7xl mx-auto">

    <div className="text-center mb-20">

      <p className="text-cyan-400 uppercase tracking-[0.35em] text-xs mb-6">
        Autonomous Intelligence Layer
      </p>

      <h2 className="text-5xl md:text-7xl font-black leading-tight mb-8">

        AI Proposal
        <br />

        Generator Runtime

      </h2>

      <p className="text-zinc-400 text-xl max-w-3xl mx-auto leading-relaxed">

        Simulate autonomous proposal generation powered by the PhantomOps infrastructure runtime.

      </p>

    </div>

    <div className="grid lg:grid-cols-2 gap-10 items-start">

      {/* LEFT PANEL */}

      <div className="relative overflow-hidden rounded-[32px] border border-cyan-500/20 bg-white/[0.03] backdrop-blur-2xl p-10 shadow-[0_0_80px_rgba(34,211,238,0.08)]">

        <div className="absolute inset-0 opacity-30 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.18),transparent_60%)]" />

        <div className="relative z-10">

          <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-8">
            Proposal Input
          </p>

          <div className="space-y-6">

            <input
              type="text"
              placeholder="Company Name"
              value={proposalData.company}
              onChange={(e) =>
                setProposalData({
                  ...proposalData,
                  company: e.target.value,
                })
              }
              className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
            />

            <input
              type="text"
              placeholder="Business Requirement"
              value={proposalData.requirement}
              onChange={(e) =>
                setProposalData({
                  ...proposalData,
                  requirement: e.target.value,
                })
              }
              className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
            />

            <select
              value={proposalData.budget}
              onChange={(e) =>
                setProposalData({
                  ...proposalData,
                  budget: e.target.value,
                })
              }
              className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
            >

              <option value="">Select Budget</option>
              <option>$5k - $15k</option>
              <option>$15k - $50k</option>
              <option>$50k - $100k</option>
              <option>$100k+</option>

            </select>

            <button
              onClick={() => setProposalGenerated(true)}
              className="group relative overflow-hidden w-full rounded-2xl bg-cyan-400 px-8 py-5 text-black font-black hover:scale-[1.02] transition-all duration-300 hover:shadow-[0_0_60px_rgba(34,211,238,0.35)]"
            >

              <span className="relative z-10">
                Generate AI Proposal
              </span>

              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.55),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

            </button>

          </div>

        </div>

      </div>

      {/* RIGHT PANEL */}

      <div className="relative overflow-hidden rounded-[32px] border border-white/10 bg-white/[0.03] backdrop-blur-2xl p-10 min-h-[500px]">

        <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.15),transparent_60%)]" />

        <div className="relative z-10">

          <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-8">
            Runtime Output
          </p>

          {proposalLoading ? (

  <div className="h-[350px] flex flex-col items-center justify-center border border-dashed border-cyan-400/20 rounded-3xl bg-cyan-400/[0.03]">

    <div className="w-16 h-16 rounded-full border-4 border-cyan-400/20 border-t-cyan-400 animate-spin mb-8" />

    <p className="text-cyan-300 text-xl font-semibold mb-4">
      Analyzing Runtime Infrastructure...
    </p>

    <div className="space-y-3 text-sm text-zinc-500 text-center">

      <p>✓ Scanning enterprise workflows</p>
      <p>✓ Calculating automation efficiency</p>
      <p>✓ Building AI deployment architecture</p>
      <p>✓ Generating operational proposal</p>

    </div>

  </div>

) : !proposalGenerated ? (

  <div className="h-[350px] flex items-center justify-center text-zinc-500 text-lg border border-dashed border-white/10 rounded-3xl">

    Awaiting AI proposal generation...

  </div>

) : (


            <div className="space-y-8">

              <div>

                <p className="text-zinc-500 text-sm mb-2">
                  Client
                </p>

                <h3 className="text-4xl font-black text-white">
                  {proposalData.company || "Enterprise Client"}
                </h3>

              </div>

             <div className="grid gap-4">

  {proposalData.company === "PhantomOps CRM Intelligence" && (
    <>
      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ AI Lead Scoring Infrastructure Activated
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Revenue Intelligence Runtime Connected
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Autonomous CRM Followup System Enabled
      </div>
    </>
  )}

  {proposalData.company === "MediOps AI" && (
    <>
      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Patient Workflow Automation Enabled
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Diagnostics Intelligence Runtime Connected
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Hospital Administration AI Activated
      </div>
    </>
  )}

  {proposalData.company === "Outreach AI" && (
    <>
      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Marketplace Intelligence Runtime Enabled
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ AI Outreach Pipeline Connected
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ WhatsApp Automation Infrastructure Active
      </div>
    </>
  )}

  {proposalData.company === "GRAM Runtime" && (
    <>
      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Multi-Agent Hierarchy Initialized
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Autonomous Runtime Orchestration Active
      </div>

      <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5">
        ✓ Operational Intelligence Infrastructure Connected
      </div>
    </>
  )}

</div>

              <div className="grid grid-cols-2 gap-5">

                <div className="rounded-2xl border border-white/10 bg-black/30 p-6">

                  <p className="text-zinc-500 text-sm mb-2">
                    Deployment Timeline
                  </p>

                  <h4 className="text-3xl font-black">
                    14 Days
                  </h4>

                </div>

                <div className="rounded-2xl border border-white/10 bg-black/30 p-6">

                  <p className="text-zinc-500 text-sm mb-2">
                    Automation Gain
                  </p>

                  <h4 className="text-3xl font-black text-cyan-400">
                    +82%
                  </h4>

                </div>

              </div>

              <div className="rounded-3xl border border-green-500/20 bg-green-500/10 p-6">

                <p className="text-green-300 text-sm uppercase tracking-[0.2em] mb-3">
                  Runtime Status
                </p>

                <h4 className="text-2xl font-black">
                  AI Proposal Generated Successfully
                </h4>

              </div>

            </div>

          )}

        </div>

      </div>

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

<footer className="relative z-10 border-t border-white/10 py-20 px-6 overflow-hidden">

  <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.08),transparent_60%)]" />

  <div className="relative z-10 max-w-7xl mx-auto">

    <div className="grid lg:grid-cols-4 gap-14 mb-16">

      {/* BRAND */}

      <div>

        <h2 className="text-3xl font-black mb-5">
          PhantomOpsAI
        </h2>

        <p className="text-zinc-400 leading-relaxed mb-6">

          Autonomous AI operations infrastructure powering intelligent business automation, outreach systems, healthcare runtimes, and enterprise orchestration.

        </p>

        <div className="inline-flex items-center gap-3 px-5 py-3 rounded-full border border-green-500/20 bg-green-500/10 text-green-300 text-sm animate-pulse">

          <div className="w-2 h-2 rounded-full bg-green-400" />

          Runtime Infrastructure Active

        </div>

      </div>

      {/* SYSTEMS */}

      <div>

        <h3 className="text-white font-bold mb-6 uppercase tracking-[0.2em] text-sm">
          Systems
        </h3>

        <div className="space-y-4 text-zinc-400">

          <p>PhantomOps CRM</p>
          <p>MediOps AI</p>
          <p>Outreach Runtime</p>
          <p>GRAM Infrastructure</p>
          <p>Proposal Intelligence</p>

        </div>

      </div>

      {/* INDUSTRIES */}

      <div>

        <h3 className="text-white font-bold mb-6 uppercase tracking-[0.2em] text-sm">
          Industries
        </h3>

        <div className="space-y-4 text-zinc-400">

          <p>Healthcare</p>
          <p>SaaS</p>
          <p>Enterprise Automation</p>
          <p>Agencies</p>
          <p>Education</p>

        </div>

      </div>

      {/* CONTACT */}

      <div>

        <h3 className="text-white font-bold mb-6 uppercase tracking-[0.2em] text-sm">
          Contact Runtime
        </h3>

        <div className="space-y-5">

          <a
            href="https://wa.me/919177334156"
            target="_blank"
            rel="noopener noreferrer"
            className="block text-zinc-300 hover:text-cyan-400 transition-all"
          >
            WhatsApp Consultation
          </a>

          <a
            href="mailto:phantomopsai@gmail.com"
            className="block text-zinc-300 hover:text-cyan-400 transition-all"
          >
            phantomopsai@gmail.com
          </a>

          <p className="text-zinc-500 text-sm leading-relaxed">

            Autonomous AI infrastructure runtime operating continuously across CRM intelligence, outreach automation, and enterprise orchestration systems.

          </p>

        </div>

      </div>

    </div>

    {/* BOTTOM */}

    <div className="flex flex-col md:flex-row items-center justify-between gap-6 border-t border-white/10 pt-8">

      <div>

        <p className="text-zinc-500 text-sm">

          © 2026 PhantomOps AI. Autonomous Infrastructure Runtime.

        </p>

      </div>

      <div className="flex items-center gap-6 text-sm text-zinc-500">

        <span>GRAM Runtime v1.0.0</span>

        <span className="text-cyan-400">
          24/7 Operational
        </span>

      </div>

    </div>

  </div>

</footer>
{/* LEAD CAPTURE MODAL */}

{showLeadModal && (

  <div className="fixed inset-0 z-[110] bg-black/80 backdrop-blur-xl flex items-center justify-center p-6">

    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="relative w-full max-w-2xl rounded-[36px] border border-cyan-500/20 bg-[#071018] p-10 backdrop-blur-2xl shadow-[0_0_80px_rgba(34,211,238,0.15)]"
    >

      <button
        onClick={() => setShowLeadModal(false)}
        className="absolute top-5 right-5 text-zinc-500 hover:text-white"
      >
        ✕
      </button>

      <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-5">
        Enterprise Automation Access
      </p>

      <h2 className="text-5xl font-black leading-tight mb-6">

        Start Your
        <span className="block text-zinc-500">
          AI Infrastructure
        </span>

      </h2>

      <p className="text-zinc-400 text-lg leading-relaxed mb-10">

        Submit your operational requirements to activate autonomous AI deployment planning.

      </p>

      <div className="space-y-5">

        <input
          type="text"
          placeholder="Full Name"
          value={leadData.name}
          onChange={(e) =>
            setLeadData({
              ...leadData,
              name: e.target.value,
            })
          }
          className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
        />

        <input
          type="email"
          placeholder="Email Address"
          value={leadData.email}
          onChange={(e) =>
            setLeadData({
              ...leadData,
              email: e.target.value,
            })
          }
          className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
        />

        <input
          type="text"
          placeholder="Company"
          value={leadData.company}
          onChange={(e) =>
            setLeadData({
              ...leadData,
              company: e.target.value,
            })
          }
          className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none focus:border-cyan-400/40"
        />

        <textarea
          placeholder="Describe your automation requirements..."
          rows="5"
          value={leadData.requirement}
          onChange={(e) =>
            setLeadData({
              ...leadData,
              requirement: e.target.value,
            })
          }
          className="w-full rounded-2xl border border-white/10 bg-black/30 px-6 py-5 text-white outline-none resize-none focus:border-cyan-400/40"
        />

        <button
          onClick={() => {

  const message = `Hello PhantomOps AI,

Name: ${leadData.name}
Email: ${leadData.email}
Company: ${leadData.company}

Requirement:
${leadData.requirement}

I want to activate AI infrastructure deployment.`;

  window.open(
    `https://wa.me/919177334156?text=${encodeURIComponent(message)}`,
    "_blank"
  );

  setShowLeadModal(false);

}}
          className="group relative overflow-hidden w-full rounded-2xl bg-cyan-400 px-8 py-5 text-black font-black hover:scale-[1.02] transition-all duration-300 hover:shadow-[0_0_60px_rgba(34,211,238,0.35)]"
        >

          <span className="relative z-10">
            Activate AI Deployment
          </span>

          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-all duration-700 bg-[linear-gradient(120deg,transparent,rgba(255,255,255,0.55),transparent)] translate-x-[-120%] group-hover:translate-x-[120%]" />

        </button>

      </div>

    </motion.div>

  </div>

)}
{/* CRM MODAL */}
{showCRM && (

  <div className="fixed inset-0 z-[100] bg-black/80 backdrop-blur-xl flex items-center justify-center p-6">

    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-[#0b1120] border border-cyan-500/20 rounded-[32px] max-w-6xl w-full p-10 relative shadow-[0_0_80px_rgba(34,211,238,0.15)]"
    >

      <button
        onClick={() => setShowCRM(false)}
        className="absolute top-5 right-5 text-zinc-400 hover:text-white"
      >
        ✕
      </button>

      <div className="mb-10">

        <p className="text-cyan-400 uppercase tracking-[0.3em] text-xs mb-4">
          AI CRM Infrastructure
        </p>

        <h2 className="text-5xl font-black">
          PhantomOps CRM
        </h2>

      </div>

      <div className="overflow-auto rounded-3xl border border-white/10 bg-black/20">

        <table className="w-full text-left min-w-[900px]">

          <thead>

            <tr className="border-b border-white/10">

              <th className="p-5">Lead</th>
              <th className="p-5">System</th>
              <th className="p-5">Requirement</th>
              <th className="p-5">Status</th>
              <th className="p-5">AI Score</th>

            </tr>

          </thead>

          <tbody>

            {[
              {
                name: "Ramesh",
                company: "PhantomOps",
                requirement: "Autonomous AI Infrastructure",
                status: "HIGH PRIORITY",
                score: "98%",
              },
              {
                name: "MediCore Hospitals",
                company: "MediOps AI",
                requirement: "Hospital Workflow Automation",
                status: "ACTIVE",
                score: "94%",
              },
              {
                name: "ScaleFlow Ventures",
                company: "Outreach AI",
                requirement: "AI Revenue Operations",
                status: "PROPOSAL SENT",
                score: "91%",
              },
            ].map((lead, index) => (

              <tr
                key={index}
                className="border-b border-white/5 hover:bg-white/5 transition-all"
              >

                <td className="p-5">
                  {lead.name}
                </td>

                <td className="p-5 text-cyan-400">
                  {lead.company}
                </td>

                <td className="p-5 text-zinc-300">
                  {lead.requirement}
                </td>

                <td className="p-5">

                  <span className="px-3 py-1 rounded-full text-xs bg-green-500/10 border border-green-500/20 text-green-300">
                    {lead.status}
                  </span>

                </td>

                <td className="p-5 text-cyan-300">
                  {lead.score}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </motion.div>

  </div>

)}

</div>

);
}